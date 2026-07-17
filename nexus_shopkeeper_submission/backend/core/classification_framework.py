"""
Nexus Shopkeeper - Phase 1: Rule-Based Customer Classification Framework
Defines explicit rules and thresholds to classify customer profiles into 
one of the six behavioral segments, and provides a fallback profile-distance classifier.
"""

import json
import math
import sys
from pathlib import Path
from typing import Dict, List, Any

# Add project root to python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from data.schemas.customer_schema import CustomerProfile, CustomerFeatures
from backend.core.support import atomic_write_json


# Segment definitions and their approximate center values (from dataset generator)
SEGMENT_CENTERS = {
    "Ultra-Luxury Spender": {
        "total_spend": 32000.0, "avg_transaction_value": 210.0, "visit_frequency": 10.0,
        "days_since_last_visit": 5.0, "luxury_item_ratio": 0.72, "bulk_purchase_score": 0.15,
        "discount_usage_rate": 0.08, "impulse_buy_score": 0.40, "brand_loyalty_index": 0.85,
        "price_sensitivity": 0.10, "category_diversity": 0.65, "peak_hour_shopping": 0.35,
        "return_rate": 0.05, "credit_utilization": 0.25, "seasonal_variation": 0.50,
        "engagement_score": 0.80
    },
    "Mid-Tier Consistent": {
        "total_spend": 9500.0, "avg_transaction_value": 65.0, "visit_frequency": 14.0,
        "days_since_last_visit": 4.0, "luxury_item_ratio": 0.18, "bulk_purchase_score": 0.35,
        "discount_usage_rate": 0.30, "impulse_buy_score": 0.25, "brand_loyalty_index": 0.72,
        "price_sensitivity": 0.45, "category_diversity": 0.70, "peak_hour_shopping": 0.55,
        "return_rate": 0.08, "credit_utilization": 0.40, "seasonal_variation": 0.35,
        "engagement_score": 0.55
    },
    "High-Value Impulse": {
        "total_spend": 14000.0, "avg_transaction_value": 120.0, "visit_frequency": 8.0,
        "days_since_last_visit": 8.0, "luxury_item_ratio": 0.40, "bulk_purchase_score": 0.12,
        "discount_usage_rate": 0.15, "impulse_buy_score": 0.78, "brand_loyalty_index": 0.45,
        "price_sensitivity": 0.25, "category_diversity": 0.80, "peak_hour_shopping": 0.60,
        "return_rate": 0.15, "credit_utilization": 0.20, "seasonal_variation": 0.55,
        "engagement_score": 0.70
    },
    "Essential Bulk Buyer": {
        "total_spend": 7500.0, "avg_transaction_value": 95.0, "visit_frequency": 6.0,
        "days_since_last_visit": 12.0, "luxury_item_ratio": 0.05, "bulk_purchase_score": 0.82,
        "discount_usage_rate": 0.40, "impulse_buy_score": 0.10, "brand_loyalty_index": 0.60,
        "price_sensitivity": 0.55, "category_diversity": 0.35, "peak_hour_shopping": 0.30,
        "return_rate": 0.03, "credit_utilization": 0.50, "seasonal_variation": 0.20,
        "engagement_score": 0.35
    },
    "Strict Budget Spender": {
        "total_spend": 2200.0, "avg_transaction_value": 22.0, "visit_frequency": 10.0,
        "days_since_last_visit": 6.0, "luxury_item_ratio": 0.02, "bulk_purchase_score": 0.25,
        "discount_usage_rate": 0.55, "impulse_buy_score": 0.08, "brand_loyalty_index": 0.50,
        "price_sensitivity": 0.88, "category_diversity": 0.40, "peak_hour_shopping": 0.45,
        "return_rate": 0.12, "credit_utilization": 0.65, "seasonal_variation": 0.30,
        "engagement_score": 0.25
    },
    "Strategic Deal-Hunter": {
        "total_spend": 6500.0, "avg_transaction_value": 55.0, "visit_frequency": 12.0,
        "days_since_last_visit": 5.0, "luxury_item_ratio": 0.22, "bulk_purchase_score": 0.45,
        "discount_usage_rate": 0.85, "impulse_buy_score": 0.30, "brand_loyalty_index": 0.38,
        "price_sensitivity": 0.72, "category_diversity": 0.75, "peak_hour_shopping": 0.50,
        "return_rate": 0.10, "credit_utilization": 0.55, "seasonal_variation": 0.60,
        "engagement_score": 0.72
    }
}


def classify_customer(features: CustomerFeatures) -> str:
    """
    Classifies a customer based on 16 feature rules.
    If the rule matches are ambiguous, falls back to Euclidean distance to segment centers.
    """
    # 1. Check Ultra-Luxury Spender
    if (features.total_spend > 20000 and 
            features.luxury_item_ratio > 0.5 and 
            features.price_sensitivity < 0.25):
        return "Ultra-Luxury Spender"

    # 2. Check Strict Budget Spender
    if (features.price_sensitivity > 0.75 and 
            features.total_spend < 4500 and 
            features.luxury_item_ratio < 0.1):
        return "Strict Budget Spender"

    # 3. Check Strategic Deal-Hunter
    if (features.discount_usage_rate > 0.7 and 
            features.price_sensitivity > 0.5):
        return "Strategic Deal-Hunter"

    # 4. Check Essential Bulk Buyer
    if (features.bulk_purchase_score > 0.65 and 
            features.category_diversity < 0.55):
        return "Essential Bulk Buyer"

    # 5. Check High-Value Impulse
    if (features.impulse_buy_score > 0.65 and 
            features.avg_transaction_value > 80):
        return "High-Value Impulse"

    # 6. Check Mid-Tier Consistent
    if (features.brand_loyalty_index > 0.6 and 
            features.visit_frequency > 9 and 
            features.total_spend > 4000):
        return "Mid-Tier Consistent"

    # Fallback: Euclidean Distance Classifier (Normalized using typical ranges)
    # Define approximate feature min-max ranges for normalization
    feature_ranges = {
        "total_spend": (0.0, 50000.0),
        "avg_transaction_value": (0.0, 350.0),
        "visit_frequency": (0.0, 30.0),
        "days_since_last_visit": (0.0, 30.0),
        "luxury_item_ratio": (0.0, 1.0),
        "bulk_purchase_score": (0.0, 1.0),
        "discount_usage_rate": (0.0, 1.0),
        "impulse_buy_score": (0.0, 1.0),
        "brand_loyalty_index": (0.0, 1.0),
        "price_sensitivity": (0.0, 1.0),
        "category_diversity": (0.0, 1.0),
        "peak_hour_shopping": (0.0, 1.0),
        "return_rate": (0.0, 1.0),
        "credit_utilization": (0.0, 1.0),
        "seasonal_variation": (0.0, 1.0),
        "engagement_score": (0.0, 1.0)
    }

    best_segment = "Mid-Tier Consistent"
    min_dist = float("inf")

    # Get customer values
    cust_vals = features.dict()

    for seg_name, center in SEGMENT_CENTERS.items():
        dist_sq = 0.0
        for feat, center_val in center.items():
            c_val = cust_vals[feat]
            f_min, f_max = feature_ranges[feat]
            # Min-Max normalization
            norm_c = (c_val - f_min) / (f_max - f_min)
            norm_center = (center_val - f_min) / (f_max - f_min)
            dist_sq += (norm_c - norm_center) ** 2
        
        dist = math.sqrt(dist_sq)
        if dist < min_dist:
            min_dist = dist
            best_segment = seg_name

    return best_segment


def classify_all(customers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Classifies all customers in the list and updates their segment_label."""
    updated_customers = []
    for cust_dict in customers:
        profile = CustomerProfile(**cust_dict)
        label = classify_customer(profile.features)
        profile.segment_label = label
        updated_customers.append(profile.dict())
    return updated_customers


def main():
    print("========================================================================")
    print("  NEXUS SHOPKEEPER - Phase 1 Rule-Based Classification Framework")
    print("========================================================================")

    customers_file = PROJECT_ROOT / "data" / "raw" / "customers.json"
    if not customers_file.exists():
        print(f"Error: Customers file does not exist at {customers_file}")
        sys.exit(1)

    with open(customers_file, "r", encoding="utf-8") as f:
        customers = json.load(f)

    print(f"Loaded {len(customers)} customers.")
    classified = classify_all(customers)

    # Calculate distributions
    counts = {}
    correct_matches = 0
    for original, updated in zip(customers, classified):
        label = updated["segment_label"]
        counts[label] = counts.get(label, 0) + 1
        
        # Verify against generation label (which was set during synthetic gen but can be checked)
        # Note: check if generate_dataset set a truth label we can compare
        # (in synthetic dataset we generated them per segment)
        # Let's see if generate_dataset saved the label
        orig_label = original.get("segment_label")
        if orig_label == label:
            correct_matches += 1

    print("\nRule-Based Classification Segment Distribution:")
    for label, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        pct = (count / len(classified)) * 100
        print(f"  {label:30} : {count:3d} ({pct:.1f}%)")

    accuracy = (correct_matches / len(classified)) * 100
    print(f"\nRule Alignment Accuracy (vs original generation tags): {accuracy:.1f}%")

    # Save rule-based results
    output_path = PROJECT_ROOT / "data" / "processed"
    output_path.mkdir(parents=True, exist_ok=True)
    atomic_write_json(output_path / "customers_classified_rules.json", classified)
    print(f"Saved rule-classified profiles to: {output_path / 'customers_classified_rules.json'}")


if __name__ == "__main__":
    import math
    main()
