"""
Nexus Shopkeeper - Phase 2: Vectorized 16-Dimensional K-Means Clustering Engine
================================================================================
Pure NumPy implementation of K-Means with k-means++ initialization,
silhouette score computation, optimal K selection, and retail segment mapping.
"""

import numpy as np
import json
import os
import sys
import time
from typing import List, Tuple, Dict, Optional, Any

# ─── Project paths ───────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

# ─── Segment names mapped by spending profile ───────────────────────────────
SEGMENT_NAMES = [
    "Ultra-Luxury Spender",
    "Mid-Tier Consistent",
    "High-Value Impulse",
    "Essential Bulk Buyer",
    "Strict Budget Spender",
    "Strategic Deal-Hunter",
]

# ─── 16 feature columns that Phase 1 generates for each customer ────────────
FEATURE_COLUMNS = [
    "total_spend", "avg_transaction_value", "visit_frequency",
    "days_since_last_visit", "luxury_item_ratio", "bulk_purchase_score",
    "discount_usage_rate", "impulse_buy_score", "brand_loyalty_index",
    "price_sensitivity", "category_diversity", "peak_hour_shopping",
    "return_rate", "credit_utilization", "seasonal_variation",
    "engagement_score",
]


# ═══════════════════════════════════════════════════════════════════════════════
#  SYNTHETIC DATA GENERATOR  (used when Phase 1 data is not yet available)
# ═══════════════════════════════════════════════════════════════════════════════

def _generate_synthetic_customers(n: int = 200, seed: int = 42) -> Tuple[List[dict], np.ndarray]:
    """
    Creates *n* synthetic customers with 16-dimensional feature vectors.
    Each customer belongs to a latent archetype so the clustering has real
    structure to discover.
    """
    rng = np.random.RandomState(seed)

    # Archetype centres (6 archetypes × 16 features)
    archetype_centers = np.array([
        # Ultra-Luxury:  high spend, high avg, few txns, high max, high min, low freq, many cats, low disc, low return
        [15000, 750, 20, 3000, 200, 5, 12, 0.25, 0.05, 0.02, 6.0, 8000, 900, 10, 2000, 4.8],
        # Mid-Tier:      moderate across the board
        [4000,  120, 35, 500,  30,  10, 8,  0.35, 0.15, 0.05, 4.0, 3000, 600, 30, 500,  4.2],
        # High-Value Impulse: high spend, many txns, high discount use
        [8000,  200, 50, 1200, 15,  3,  15, 0.20, 0.40, 0.10, 5.5, 5000, 400, 5,  800,  3.8],
        # Essential Bulk: moderate spend, few txns, large basket, low variety
        [6000,  400, 15, 800,  100, 20, 4,  0.60, 0.10, 0.03, 12., 2500, 800, 45, 300,  4.5],
        # Strict Budget:  low spend, small basket, high disc, many returns
        [800,   25,  40, 80,   5,   8,  5,  0.45, 0.70, 0.15, 2.0, 500,  300, 60, 50,   3.5],
        # Deal-Hunter:    moderate spend, very high disc, moderate returns
        [2500,  80,  30, 400,  10,  7,  10, 0.30, 0.55, 0.08, 3.5, 1500, 500, 20, 200,  3.9],
    ], dtype=np.float64)

    # Noise scale for each feature (proportional to centre magnitude)
    noise_scales = archetype_centers.std(axis=0) * 0.35

    customers = []
    features_list = []

    for i in range(n):
        archetype_idx = i % 6
        centre = archetype_centers[archetype_idx]
        noise = rng.randn(16) * noise_scales
        raw = np.abs(centre + noise)  # keep positive

        # Clamp rates to [0, 1]
        for rate_col in [7, 8, 9]:
            raw[rate_col] = np.clip(raw[rate_col], 0.0, 1.0)
        # Clamp rating to [1, 5]
        raw[15] = np.clip(raw[15], 1.0, 5.0)
        # Integers
        for int_col in [2, 6, 11, 12, 13]:
            raw[int_col] = max(1, int(round(raw[int_col])))

        features_list.append(raw)

        cust = {
            "customer_id": f"CUST-{i+1:04d}",
            "name": f"Customer_{i+1}",
            "email": f"customer{i+1}@nexus.shop",
            "segment": "unassigned",
            "features": {FEATURE_COLUMNS[j]: float(round(raw[j], 4)) for j in range(16)},
        }
        customers.append(cust)

    return customers, np.array(features_list, dtype=np.float64)


# ═══════════════════════════════════════════════════════════════════════════════
#  K-MEANS ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class KMeansEngine:
    """
    Vectorized K-Means clustering engine operating on 16-D customer feature
    space.  Implements k-means++ seeding, silhouette scoring, elbow analysis,
    and automatic segment-name mapping.
    """

    def __init__(
        self,
        n_clusters: int = 6,
        max_iterations: int = 300,
        tolerance: float = 1e-6,
        random_state: int = 42,
    ):
        self.n_clusters = n_clusters
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.random_state = random_state

        # Fitted state
        self.centroids: Optional[np.ndarray] = None
        self.labels_: Optional[np.ndarray] = None
        self.inertia_: float = 0.0
        self.n_iterations_: int = 0
        self.convergence_history: List[float] = []

        # Normalisation params
        self._min: Optional[np.ndarray] = None
        self._range: Optional[np.ndarray] = None

    # ── Normalisation helpers ────────────────────────────────────────────────

    def _fit_normalize(self, data: np.ndarray) -> np.ndarray:
        """Min-max scale to [0, 1].  Stores params for later transform."""
        self._min = data.min(axis=0)
        self._range = data.max(axis=0) - self._min
        self._range[self._range == 0] = 1.0  # avoid div-by-zero
        return (data - self._min) / self._range

    def _transform_normalize(self, data: np.ndarray) -> np.ndarray:
        """Apply previously fitted min-max scaling."""
        if self._min is None:
            raise RuntimeError("Normalizer not fitted.  Call fit() first.")
        return (data - self._min) / self._range

    # ── K-Means++ initialisation ─────────────────────────────────────────────

    def _initialize_centroids(self, data: np.ndarray) -> np.ndarray:
        """
        K-means++ centroid seeding for better convergence.
        1. Pick first centroid uniformly at random.
        2. For each remaining centroid pick the point whose minimum squared
           distance to existing centroids is maximal (probability-weighted).
        """
        rng = np.random.RandomState(self.random_state)
        n_samples, n_features = data.shape
        centroids = np.empty((self.n_clusters, n_features), dtype=np.float64)

        # First centroid – random sample
        idx = rng.randint(0, n_samples)
        centroids[0] = data[idx]

        for c in range(1, self.n_clusters):
            # Squared distances to nearest existing centroid
            dists = np.min(
                np.sum((data[:, np.newaxis, :] - centroids[np.newaxis, :c, :]) ** 2, axis=2),
                axis=1,
            )
            # Weighted probability
            probs = dists / dists.sum()
            cumulative = np.cumsum(probs)
            r = rng.rand()
            idx = int(np.searchsorted(cumulative, r))
            idx = min(idx, n_samples - 1)
            centroids[c] = data[idx]

        return centroids

    # ── Core K-Means steps ───────────────────────────────────────────────────

    def _assign_clusters(self, data: np.ndarray) -> np.ndarray:
        """Assign each point to the nearest centroid (vectorized)."""
        # data: (N, D),  centroids: (K, D)
        # diff: (N, K, D)
        diff = data[:, np.newaxis, :] - self.centroids[np.newaxis, :, :]
        sq_dists = np.sum(diff ** 2, axis=2)           # (N, K)
        return np.argmin(sq_dists, axis=1)              # (N,)

    def _update_centroids(self, data: np.ndarray, labels: np.ndarray) -> np.ndarray:
        """Recompute centroids as mean of assigned points."""
        new_centroids = np.empty_like(self.centroids)
        for k in range(self.n_clusters):
            members = data[labels == k]
            if len(members) == 0:
                # Re-initialise dead centroid to a random data point
                rng = np.random.RandomState(self.random_state + k)
                new_centroids[k] = data[rng.randint(0, len(data))]
            else:
                new_centroids[k] = members.mean(axis=0)
        return new_centroids

    def _calculate_inertia(self, data: np.ndarray, labels: np.ndarray) -> float:
        """Sum of squared distances of samples to their closest centroid."""
        diffs = data - self.centroids[labels]
        return float(np.sum(diffs ** 2))

    # ── Fit / Predict ────────────────────────────────────────────────────────

    def fit(self, data: np.ndarray) -> "KMeansEngine":
        """
        Run K-Means on *data* (N × D).  Normalises internally.
        """
        print(f"\n{'='*70}")
        print(f"  K-Means Engine  |  K={self.n_clusters}  |  max_iter={self.max_iterations}")
        print(f"  Data shape: {data.shape}")
        print(f"{'='*70}")

        normed = self._fit_normalize(data)
        self.centroids = self._initialize_centroids(normed)

        t0 = time.perf_counter()
        for i in range(1, self.max_iterations + 1):
            labels = self._assign_clusters(normed)
            new_centroids = self._update_centroids(normed, labels)

            shift = np.sqrt(np.sum((new_centroids - self.centroids) ** 2))
            inertia = self._calculate_inertia(normed, labels)
            self.convergence_history.append(inertia)

            self.centroids = new_centroids
            self.labels_ = labels
            self.inertia_ = inertia
            self.n_iterations_ = i

            if i <= 10 or i % 25 == 0:
                print(f"  iter {i:>4d}  |  inertia = {inertia:12.4f}  |  shift = {shift:.8f}")

            if shift < self.tolerance:
                print(f"  ✓ Converged at iteration {i}  (shift {shift:.2e} < tol {self.tolerance})")
                break

        elapsed = time.perf_counter() - t0
        print(f"  Time: {elapsed:.3f}s  |  Final inertia: {self.inertia_:.4f}")
        self._print_cluster_sizes(labels)
        return self

    def predict(self, data: np.ndarray) -> np.ndarray:
        """Predict nearest cluster for new data."""
        normed = self._transform_normalize(data)
        return self._assign_clusters(normed)

    def fit_predict(self, data: np.ndarray) -> np.ndarray:
        """Fit then return labels."""
        self.fit(data)
        return self.labels_

    # ── Silhouette Score (from scratch) ──────────────────────────────────────

    def calculate_silhouette_score(self, data: np.ndarray, labels: np.ndarray) -> float:
        """
        Full silhouette coefficient computed from scratch.

        For each sample i:
          a(i) = mean intra-cluster distance
          b(i) = min over other clusters of mean distance to that cluster
          s(i) = (b(i) - a(i)) / max(a(i), b(i))
        Score = mean of s(i).

        Uses vectorized distance computation; for very large N a sampled
        approximation is used to keep runtime manageable.
        """
        normed = self._transform_normalize(data)
        n = len(normed)
        unique_labels = np.unique(labels)
        k = len(unique_labels)

        if k <= 1 or k >= n:
            return 0.0

        # For large datasets, subsample
        max_samples = 2000
        if n > max_samples:
            rng = np.random.RandomState(self.random_state)
            idx = rng.choice(n, max_samples, replace=False)
            normed = normed[idx]
            labels = labels[idx]
            n = max_samples

        # Pairwise distance matrix (N x N)
        # Using ||x-y||^2 = ||x||^2 + ||y||^2 - 2 x·y
        sq_norms = np.sum(normed ** 2, axis=1)
        dist_sq = sq_norms[:, None] + sq_norms[None, :] - 2.0 * normed @ normed.T
        dist_sq = np.maximum(dist_sq, 0.0)
        dist_mat = np.sqrt(dist_sq)

        sil = np.zeros(n, dtype=np.float64)

        for i in range(n):
            own_label = labels[i]
            own_mask = labels == own_label
            own_count = own_mask.sum()

            # a(i): mean distance to own cluster (excluding self)
            if own_count <= 1:
                a_i = 0.0
            else:
                a_i = dist_mat[i, own_mask].sum() / (own_count - 1)

            # b(i): min mean distance to any other cluster
            b_i = np.inf
            for lbl in unique_labels:
                if lbl == own_label:
                    continue
                other_mask = labels == lbl
                other_count = other_mask.sum()
                if other_count == 0:
                    continue
                mean_dist = dist_mat[i, other_mask].mean()
                if mean_dist < b_i:
                    b_i = mean_dist

            denom = max(a_i, b_i)
            sil[i] = (b_i - a_i) / denom if denom > 0 else 0.0

        score = float(np.mean(sil))
        return score

    # ── Cluster Statistics ───────────────────────────────────────────────────

    def get_cluster_statistics(self, data: np.ndarray, labels: np.ndarray, segment_map: Optional[Dict[int, str]] = None) -> Dict[str, Any]:
        """
        Per-cluster statistics: size, centroid (original scale), std, min, max
        for each of the 16 features.
        """
        stats: Dict[str, Any] = {}
        for k in range(self.n_clusters):
            mask = labels == k
            members = data[mask]
            if segment_map and k in segment_map:
                segment_name = segment_map[k]
            else:
                segment_name = SEGMENT_NAMES[k] if k < len(SEGMENT_NAMES) else f"Segment-{k}"
            if len(members) == 0:
                stats[segment_name] = {"size": 0}
                continue
            stats[segment_name] = {
                "cluster_id": int(k),
                "size": int(mask.sum()),
                "centroid_mean": {FEATURE_COLUMNS[j]: round(float(members[:, j].mean()), 4)
                                  for j in range(min(16, data.shape[1]))},
                "centroid_std": {FEATURE_COLUMNS[j]: round(float(members[:, j].std()), 4)
                                 for j in range(min(16, data.shape[1]))},
                "feature_min": {FEATURE_COLUMNS[j]: round(float(members[:, j].min()), 4)
                                for j in range(min(16, data.shape[1]))},
                "feature_max": {FEATURE_COLUMNS[j]: round(float(members[:, j].max()), 4)
                                for j in range(min(16, data.shape[1]))},
            }
        return stats

    # ── Optimal K (Elbow + Silhouette) ───────────────────────────────────────

    def find_optimal_k(self, data: np.ndarray, k_range: Tuple[int, int] = (2, 10)) -> int:
        """
        Tests each K in *k_range*, computes inertia (elbow) and silhouette
        score, then selects K by highest silhouette with tie-break towards
        lower K.
        """
        print(f"\n{'─'*60}")
        print("  Searching for optimal K ...")
        print(f"{'─'*60}")

        results: List[Dict[str, Any]] = []

        for k in range(k_range[0], k_range[1] + 1):
            eng = KMeansEngine(n_clusters=k, max_iterations=self.max_iterations,
                               tolerance=self.tolerance, random_state=self.random_state)
            labels = eng.fit_predict(data)
            sil = eng.calculate_silhouette_score(data, labels)
            results.append({"k": k, "inertia": eng.inertia_, "silhouette": sil})
            print(f"  K={k:>2d}  |  inertia={eng.inertia_:10.4f}  |  silhouette={sil:.4f}")

        # Pick K with best silhouette
        best = max(results, key=lambda r: r["silhouette"])
        print(f"\n  ★ Optimal K = {best['k']}  (silhouette = {best['silhouette']:.4f})")
        return best["k"]

    # ── Segment Mapping ──────────────────────────────────────────────────────

    def map_segments(self, data: np.ndarray, labels: np.ndarray) -> Dict[int, str]:
        """
        Map cluster indices to the 6 retail segment names by computing the 
        Euclidean distance of each centroid to the known archetype centers
        in normalized 16-D feature space.
        """
        archetypes = {
            "Ultra-Luxury Spender": [32000.0, 210.0, 10.0, 5.0, 0.72, 0.15, 0.08, 0.40, 0.85, 0.10, 0.65, 0.35, 0.05, 0.25, 0.50, 0.80],
            "Mid-Tier Consistent": [9500.0, 65.0, 14.0, 4.0, 0.18, 0.35, 0.30, 0.25, 0.72, 0.45, 0.70, 0.55, 0.08, 0.40, 0.35, 0.55],
            "High-Value Impulse": [14000.0, 120.0, 8.0, 8.0, 0.40, 0.12, 0.15, 0.78, 0.45, 0.25, 0.80, 0.60, 0.15, 0.20, 0.55, 0.70],
            "Essential Bulk Buyer": [7500.0, 95.0, 6.0, 12.0, 0.05, 0.82, 0.40, 0.10, 0.60, 0.55, 0.35, 0.30, 0.03, 0.50, 0.20, 0.35],
            "Strict Budget Spender": [2200.0, 22.0, 10.0, 6.0, 0.02, 0.25, 0.55, 0.08, 0.50, 0.88, 0.40, 0.45, 0.12, 0.65, 0.30, 0.25],
            "Strategic Deal-Hunter": [6500.0, 55.0, 12.0, 5.0, 0.22, 0.45, 0.85, 0.30, 0.38, 0.72, 0.75, 0.50, 0.10, 0.55, 0.60, 0.72]
        }

        # Min-max range of the input data for normalization
        d_min = data.min(axis=0)
        d_max = data.max(axis=0)
        d_range = d_max - d_min
        d_range[d_range == 0] = 1.0

        # Compute cluster centroids
        centroids = np.zeros((self.n_clusters, data.shape[1]))
        for k in range(self.n_clusters):
            members = data[labels == k]
            if len(members) > 0:
                centroids[k] = members.mean(axis=0)

        # Normalize centroids
        norm_centroids = (centroids - d_min) / d_range

        mapping = {}
        available_segments = list(archetypes.keys())
        
        # Distance matrix (K, 6)
        dist_matrix = np.zeros((self.n_clusters, len(available_segments)))
        for k in range(self.n_clusters):
            norm_c = norm_centroids[k]
            for s_idx, seg_name in enumerate(available_segments):
                arch_vec = np.array(archetypes[seg_name])
                norm_arch = (arch_vec - d_min) / d_range
                dist_matrix[k, s_idx] = np.sqrt(np.sum((norm_c - norm_arch) ** 2))

        # Greedy unique mapping
        assigned_segments = set()
        for k in range(self.n_clusters):
            sorted_segments = sorted(
                range(len(available_segments)), 
                key=lambda s_idx: dist_matrix[k, s_idx]
            )
            assigned = False
            for s_idx in sorted_segments:
                seg_name = available_segments[s_idx]
                if seg_name not in assigned_segments:
                    mapping[k] = seg_name
                    assigned_segments.add(seg_name)
                    assigned = True
                    break
            if not assigned:
                closest_s_idx = sorted_segments[0]
                mapping[k] = available_segments[closest_s_idx]
        
        return mapping

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _print_cluster_sizes(self, labels: np.ndarray) -> None:
        unique, counts = np.unique(labels, return_counts=True)
        print("  Cluster sizes:")
        for u, c in zip(unique, counts):
            bar = "█" * (c // 2)
            print(f"    cluster {u}: {c:>5d}  {bar}")

    # ── Persistence ──────────────────────────────────────────────────────────

    def save_results(
        self,
        data: np.ndarray,
        labels: np.ndarray,
        output_dir: Optional[str] = None,
    ) -> Dict[str, str]:
        """Save feature matrix, labels, and centroids to .npy files."""
        out = output_dir or PROCESSED_DIR
        os.makedirs(out, exist_ok=True)

        paths = {
            "customer_features": os.path.join(out, "customer_features.npy"),
            "cluster_labels": os.path.join(out, "cluster_labels.npy"),
            "cluster_centroids": os.path.join(out, "cluster_centroids.npy"),
        }
        np.save(paths["customer_features"], data)
        np.save(paths["cluster_labels"], labels)
        np.save(paths["cluster_centroids"], self.centroids)

        for name, p in paths.items():
            print(f"  Saved {name} → {p}")

        return paths


# ═══════════════════════════════════════════════════════════════════════════════
#  STANDALONE EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

def load_customer_features() -> Tuple[List[dict], np.ndarray]:
    """Load customer data from Phase 1 JSON or generate synthetic."""
    customers_path = os.path.join(RAW_DIR, "customers.json")
    if os.path.exists(customers_path):
        print(f"  Loading customers from {customers_path}")
        with open(customers_path, "r") as f:
            customers = json.load(f)
        # Extract 16-D feature vectors
        features = []
        for c in customers:
            feat = c.get("features", {})
            vec = [feat.get(col, 0.0) for col in FEATURE_COLUMNS]
            features.append(vec)
        return customers, np.array(features, dtype=np.float64)
    else:
        print(f"  ⚠ {customers_path} not found — generating {200} synthetic customers")
        return _generate_synthetic_customers(200)


def main() -> None:
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║     NEXUS SHOPKEEPER — K-MEANS CLUSTERING ENGINE (v2)      ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    # 1. Load data
    customers, features = load_customer_features()
    print(f"\n  Loaded {len(customers)} customers  |  Feature matrix: {features.shape}")

    # 2. Fit K-Means with K=6
    engine = KMeansEngine(n_clusters=6, max_iterations=300, tolerance=1e-6, random_state=42)
    labels = engine.fit_predict(features)

    # 3. Silhouette score
    sil = engine.calculate_silhouette_score(features, labels)
    print(f"\n  ★ Silhouette Score: {sil:.4f}")

    # 4. Map segments
    segment_map = engine.map_segments(features, labels)
    print("\n  Segment Mapping:")
    for cid, name in sorted(segment_map.items()):
        count = int((labels == cid).sum())
        print(f"    Cluster {cid} → {name}  ({count} customers)")

    # 5. Cluster statistics
    stats = engine.get_cluster_statistics(features, labels, segment_map)
    print("\n  Cluster Statistics (excerpt):")
    for seg_name, info in stats.items():
        if info.get("size", 0) == 0:
            continue
        means = info.get("centroid_mean", {})
        print(f"    {seg_name} (n={info['size']}):")
        print(f"      avg_spent=${means.get('total_spend', 0):,.2f}  "
              f"avg_txn=${means.get('avg_transaction_value', 0):,.2f}  "
              f"disc_rate={means.get('discount_usage_rate', 0):.2%}  "
              f"visit_freq={means.get('visit_frequency', 0):.1f}")

    # 6. Save
    saved = engine.save_results(features, labels)

    # 7. Also save the segment mapping JSON
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    seg_map_path = os.path.join(PROCESSED_DIR, "segment_mapping.json")
    with open(seg_map_path, "w") as f:
        json.dump({str(k): v for k, v in segment_map.items()}, f, indent=2)
    print(f"  Saved segment mapping → {seg_map_path}")

    # 8. Update customers with assigned segments
    named_labels = [segment_map.get(int(l), "Unknown") for l in labels]
    for i, cust in enumerate(customers):
        cust["segment"] = named_labels[i]
    os.makedirs(RAW_DIR, exist_ok=True)
    cust_out = os.path.join(RAW_DIR, "customers_segmented.json")
    with open(cust_out, "w") as f:
        json.dump(customers, f, indent=2)
    print(f"  Saved segmented customers → {cust_out}")

    print("\n  ✓ K-Means Engine Phase 2 complete.")


if __name__ == "__main__":
    main()
