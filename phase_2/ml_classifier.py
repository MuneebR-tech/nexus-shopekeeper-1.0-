"""
Nexus Shopkeeper - Phase 2: ML Classification Pipeline
=======================================================
Trains K-Means on an 80/20 stratified split of customer data,
evaluates classification accuracy with per-segment precision / recall / F1,
prints a confusion matrix, and exposes classify_unknown_vector() for inference.
"""

import json
import math
import os
import sys
import hashlib
import time
from typing import Dict, List, Tuple, Any, Optional

import numpy as np

# ─── Project paths ───────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

sys.path.insert(0, BASE_DIR)
from phase_2.kmeans_engine import KMeansEngine, FEATURE_COLUMNS, SEGMENT_NAMES
from backend.core.support import atomic_write_json

# ─── Valid value ranges for each of the 16 features (for clamping) ───────────
FEATURE_RANGES: Dict[str, Tuple[float, float]] = {
    "total_spend":           (0.0, 50000.0),
    "avg_transaction_value": (0.0, 5000.0),
    "visit_frequency":       (0.0, 30.0),
    "days_since_last_visit": (0.0, 365.0),
    "luxury_item_ratio":     (0.0, 1.0),
    "bulk_purchase_score":   (0.0, 1.0),
    "discount_usage_rate":   (0.0, 1.0),
    "impulse_buy_score":     (0.0, 1.0),
    "brand_loyalty_index":   (0.0, 1.0),
    "price_sensitivity":     (0.0, 1.0),
    "category_diversity":    (0.0, 1.0),
    "peak_hour_shopping":    (0.0, 1.0),
    "return_rate":           (0.0, 1.0),
    "credit_utilization":    (0.0, 1.0),
    "seasonal_variation":    (0.0, 1.0),
    "engagement_score":      (0.0, 1.0),
}

# ─── Module-level singleton (populated after first train) ────────────────────
_trained_engine: Optional[KMeansEngine] = None
_segment_map: Optional[Dict[int, str]] = None
_training_data: Optional[np.ndarray] = None


# ═══════════════════════════════════════════════════════════════════════════════
#  DATA LOADING
# ═══════════════════════════════════════════════════════════════════════════════

def load_customers() -> Tuple[List[dict], np.ndarray, List[str]]:
    """
    Load customers.json → (customer_dicts, feature_matrix, ground_truth_labels).
    """
    path = os.path.join(RAW_DIR, "customers.json")
    with open(path, "r", encoding="utf-8") as f:
        customers = json.load(f)

    features: List[List[float]] = []
    labels: List[str] = []
    for c in customers:
        feat = c.get("features", {})
        vec = [float(feat.get(col, 0.0)) for col in FEATURE_COLUMNS]
        features.append(vec)
        labels.append(c.get("segment_label", "Unknown"))

    return customers, np.array(features, dtype=np.float64), labels


# ═══════════════════════════════════════════════════════════════════════════════
#  STRATIFIED TRAIN / TEST SPLIT  (no sklearn)
# ═══════════════════════════════════════════════════════════════════════════════

def stratified_split(
    features: np.ndarray,
    labels: List[str],
    test_ratio: float = 0.20,
    seed: int = 42,
) -> Tuple[np.ndarray, np.ndarray, List[str], List[str], List[int], List[int]]:
    """
    Split data into train/test maintaining class proportions.
    Returns: X_train, X_test, y_train, y_test, train_idx, test_idx
    """
    rng = np.random.RandomState(seed)

    # Group indices by label
    label_indices: Dict[str, List[int]] = {}
    for i, lbl in enumerate(labels):
        label_indices.setdefault(lbl, []).append(i)

    train_idx: List[int] = []
    test_idx: List[int] = []

    for lbl, indices in sorted(label_indices.items()):
        arr = np.array(indices)
        rng.shuffle(arr)
        n_test = max(1, int(len(arr) * test_ratio))
        test_idx.extend(arr[:n_test].tolist())
        train_idx.extend(arr[n_test:].tolist())

    X_train = features[train_idx]
    X_test = features[test_idx]
    y_train = [labels[i] for i in train_idx]
    y_test = [labels[i] for i in test_idx]

    return X_train, X_test, y_train, y_test, train_idx, test_idx


# ═══════════════════════════════════════════════════════════════════════════════
#  MANUAL METRICS  (precision, recall, F1, confusion matrix — no sklearn)
# ═══════════════════════════════════════════════════════════════════════════════

def compute_classification_metrics(
    y_true: List[str], y_pred: List[str]
) -> Dict[str, Any]:
    """
    Compute overall accuracy, per-class precision / recall / F1,
    and a confusion matrix.  All from scratch.
    """
    all_labels = sorted(set(y_true) | set(y_pred))
    label_to_idx = {lbl: i for i, lbl in enumerate(all_labels)}
    n = len(all_labels)

    # Build confusion matrix
    cm = [[0] * n for _ in range(n)]
    for t, p in zip(y_true, y_pred):
        cm[label_to_idx[t]][label_to_idx[p]] += 1

    # Overall accuracy
    correct = sum(cm[i][i] for i in range(n))
    total = len(y_true)
    accuracy = correct / total if total > 0 else 0.0

    # Per-class metrics
    per_class: Dict[str, Dict[str, float]] = {}
    for idx, lbl in enumerate(all_labels):
        tp = cm[idx][idx]
        fp = sum(cm[r][idx] for r in range(n)) - tp
        fn = sum(cm[idx][c] for c in range(n)) - tp

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (
            2 * precision * recall / (precision + recall)
            if (precision + recall) > 0
            else 0.0
        )
        support = sum(cm[idx])

        per_class[lbl] = {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4),
            "support": support,
        }

    # Macro averages
    macro_prec = sum(v["precision"] for v in per_class.values()) / n if n else 0
    macro_rec = sum(v["recall"] for v in per_class.values()) / n if n else 0
    macro_f1 = sum(v["f1_score"] for v in per_class.values()) / n if n else 0

    return {
        "accuracy": round(accuracy, 4),
        "macro_precision": round(macro_prec, 4),
        "macro_recall": round(macro_rec, 4),
        "macro_f1": round(macro_f1, 4),
        "per_class": per_class,
        "confusion_matrix": cm,
        "labels": all_labels,
    }


def print_confusion_matrix(cm: List[List[int]], labels: List[str]) -> None:
    """Pretty-print a confusion matrix table."""
    # Abbreviate long labels
    short = []
    for lbl in labels:
        parts = lbl.split()
        abbr = "".join(p[0] for p in parts if p)
        short.append(abbr)

    col_w = max(6, max(len(s) for s in short) + 1)
    header = " " * 22 + "".join(s.rjust(col_w) for s in short)
    print(header)
    print(" " * 22 + "-" * (col_w * len(short)))

    for i, row in enumerate(cm):
        lbl_str = labels[i][:20].ljust(20)
        row_str = "".join(str(v).rjust(col_w) for v in row)
        marker = " <--" if cm[i][i] == max(row) and cm[i][i] > 0 else ""
        print(f"  {lbl_str} |{row_str}{marker}")


# ═══════════════════════════════════════════════════════════════════════════════
#  CLASSIFY UNKNOWN VECTOR
# ═══════════════════════════════════════════════════════════════════════════════

def clamp_feature_vector(raw_vector: list) -> np.ndarray:
    """
    Takes a raw 16-element list, clamps each value to its valid range.
    Handles NaN, None, non-numeric, and wrong-length inputs gracefully.
    """
    clamped = np.zeros(16, dtype=np.float64)
    for i, col in enumerate(FEATURE_COLUMNS):
        lo, hi = FEATURE_RANGES[col]
        try:
            val = float(raw_vector[i]) if i < len(raw_vector) else 0.0
            if math.isnan(val) or math.isinf(val):
                val = (lo + hi) / 2.0  # default to midpoint
        except (TypeError, ValueError, IndexError):
            val = (lo + hi) / 2.0
        clamped[i] = max(lo, min(hi, val))
    return clamped


def classify_unknown_vector(feature_vector: list) -> str:
    """
    Classify an arbitrary 16-element feature vector using the trained model.
    - Clamps values to valid ranges
    - Normalises using the trained model's min/max parameters
    - Computes Euclidean distance to each centroid
    - Returns the CLOSEST segment label (never throws, always returns valid)
    """
    global _trained_engine, _segment_map, _training_data

    # Auto-train if needed
    if _trained_engine is None:
        train_pipeline()

    engine = _trained_engine
    seg_map = _segment_map

    try:
        clamped = clamp_feature_vector(feature_vector)
        vec = clamped.reshape(1, -1)

        # Normalise using the engine's fitted min/max
        normed = engine._transform_normalize(vec)  # shape (1, 16)

        # Compute Euclidean distance to each centroid
        diffs = normed[0] - engine.centroids  # (K, 16)
        dists = np.sqrt(np.sum(diffs ** 2, axis=1))  # (K,)

        best_cluster = int(np.argmin(dists))
        label = seg_map.get(best_cluster, "Unknown")
        return label

    except Exception:
        # Absolute fallback — return the most common segment
        return SEGMENT_NAMES[0] if SEGMENT_NAMES else "Unknown"


def classify_unknown_vector_detailed(feature_vector: list) -> Dict[str, Any]:
    """
    Like classify_unknown_vector but also returns confidence and per-cluster distances.
    """
    global _trained_engine, _segment_map

    if _trained_engine is None:
        train_pipeline()

    engine = _trained_engine
    seg_map = _segment_map

    try:
        clamped = clamp_feature_vector(feature_vector)
        vec = clamped.reshape(1, -1)
        normed = engine._transform_normalize(vec)

        diffs = normed[0] - engine.centroids
        dists = np.sqrt(np.sum(diffs ** 2, axis=1))

        best_cluster = int(np.argmin(dists))
        label = seg_map.get(best_cluster, "Unknown")

        # Confidence: inverse-distance softmax style
        inv_dists = 1.0 / (dists + 1e-8)
        confidence = float(inv_dists[best_cluster] / inv_dists.sum())

        distance_map = {}
        for k in range(len(dists)):
            seg_name = seg_map.get(k, f"Cluster-{k}")
            distance_map[seg_name] = round(float(dists[k]), 6)

        return {
            "segment": label,
            "confidence": round(confidence, 4),
            "distances": distance_map,
        }
    except Exception:
        fallback = SEGMENT_NAMES[0] if SEGMENT_NAMES else "Unknown"
        return {"segment": fallback, "confidence": 0.0, "distances": {}}


# ═══════════════════════════════════════════════════════════════════════════════
#  TRAINING PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════

def train_pipeline() -> Dict[str, Any]:
    """
    Full training pipeline:
    1. Load data
    2. Stratified 80/20 split
    3. Train KMeansEngine on train set
    4. Predict on test set
    5. Map clusters → segment names
    6. Evaluate metrics
    7. Save metrics to logs/classification_metrics.json
    Returns the metrics dict.
    """
    global _trained_engine, _segment_map, _training_data

    print("\n" + "=" * 70)
    print("  ML CLASSIFICATION PIPELINE")
    print("=" * 70)

    # 1. Load
    customers, features, ground_truth = load_customers()
    n_total = len(customers)
    print(f"\n  Loaded {n_total} customers  |  Features: {features.shape}")
    label_counts: Dict[str, int] = {}
    for lbl in ground_truth:
        label_counts[lbl] = label_counts.get(lbl, 0) + 1
    print("  Ground-truth distribution:")
    for lbl, cnt in sorted(label_counts.items()):
        print(f"    {lbl}: {cnt}")

    # 2. Stratified split
    X_train, X_test, y_train, y_test, train_idx, test_idx = stratified_split(
        features, ground_truth, test_ratio=0.20, seed=42
    )
    print(f"\n  Train set: {len(y_train)}  |  Test set: {len(y_test)}")

    # 3. Train K-Means on TRAINING set only
    engine = KMeansEngine(n_clusters=6, max_iterations=300, tolerance=1e-6, random_state=42)
    train_labels = engine.fit_predict(X_train)

    # 4. Map clusters → segment names using training data
    segment_map = engine.map_segments(X_train, train_labels)
    print("\n  Segment Mapping (from training):")
    for cid, name in sorted(segment_map.items()):
        count = int((train_labels == cid).sum())
        print(f"    Cluster {cid} -> {name}  ({count} train samples)")

    # 5. Predict on test set
    test_pred_indices = engine.predict(X_test)
    y_pred = [segment_map.get(int(idx), "Unknown") for idx in test_pred_indices]

    # 6. Evaluate
    metrics = compute_classification_metrics(y_test, y_pred)

    # Store globally for classify_unknown_vector
    _trained_engine = engine
    _segment_map = segment_map
    _training_data = X_train

    # 7. Save metrics
    metrics_path = os.path.join(LOG_DIR, "classification_metrics.json")
    save_metrics = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "n_total": n_total,
        "n_train": len(y_train),
        "n_test": len(y_test),
        "accuracy": metrics["accuracy"],
        "macro_precision": metrics["macro_precision"],
        "macro_recall": metrics["macro_recall"],
        "macro_f1": metrics["macro_f1"],
        "per_class": metrics["per_class"],
        "confusion_matrix": metrics["confusion_matrix"],
        "labels": metrics["labels"],
        "segment_mapping": {str(k): v for k, v in segment_map.items()},
    }
    atomic_write_json(metrics_path, save_metrics)
    print(f"\n  Metrics saved -> {metrics_path}")

    return metrics


# ═══════════════════════════════════════════════════════════════════════════════
#  PRINT REPORT
# ═══════════════════════════════════════════════════════════════════════════════

def print_report(metrics: Dict[str, Any]) -> None:
    """Pretty-print the classification report."""
    print("\n" + "=" * 70)
    print("  CLASSIFICATION REPORT")
    print("=" * 70)

    print(f"\n  Overall Accuracy: {metrics['accuracy']:.2%}")
    print(f"  Macro Precision:  {metrics['macro_precision']:.4f}")
    print(f"  Macro Recall:     {metrics['macro_recall']:.4f}")
    print(f"  Macro F1-Score:   {metrics['macro_f1']:.4f}")

    print(f"\n  {'Segment':<28s} {'Prec':>8s} {'Recall':>8s} {'F1':>8s} {'Support':>8s}")
    print("  " + "-" * 60)
    for lbl, vals in sorted(metrics["per_class"].items()):
        print(
            f"  {lbl:<28s} {vals['precision']:8.4f} {vals['recall']:8.4f} "
            f"{vals['f1_score']:8.4f} {vals['support']:8d}"
        )

    print("\n  Confusion Matrix:")
    print_confusion_matrix(metrics["confusion_matrix"], metrics["labels"])

    # Quick classify_unknown_vector demo
    print("\n  --- classify_unknown_vector demo ---")
    demo_vector = [12000, 150, 8, 5, 0.5, 0.1, 0.1, 0.8, 0.4, 0.3, 0.9, 0.5, 0.15, 0.1, 0.6, 0.7]
    result = classify_unknown_vector_detailed(demo_vector)
    print(f"  Input:  {demo_vector}")
    print(f"  Result: {result['segment']}  (confidence={result['confidence']:.2%})")
    for seg, dist in sorted(result["distances"].items(), key=lambda x: x[1]):
        print(f"    {seg:<28s}  dist={dist:.4f}")

    print("\n  Pipeline complete.\n")


# ═══════════════════════════════════════════════════════════════════════════════
#  STANDALONE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    metrics = train_pipeline()
    print_report(metrics)
