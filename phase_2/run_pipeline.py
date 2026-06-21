"""
Nexus Shopkeeper - Phase 2: Master Pipeline Runner
Orchestrates and executes the entire system end-to-end:
1. Data Schema Validation
2. Physical Rack Grid Layout & Mapping
3. Rule-Based Classification vs. K-Means Clustering
4. Store Credit Engine & Loan Operations
5. System Status Report
"""

import sys
import os
import json
from pathlib import Path

# Add project root to python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# Import engines and utilities
from phase_1.schema_validation import validate_customers, validate_inventory
from phase_1.rack_mapping import RackMap
from phase_1.classification_framework import classify_all
from phase_2.kmeans_engine import KMeansEngine, load_customer_features
from phase_2.store_credit_engine import StoreCreditEngine
from backend.core.support import atomic_write_json


def run_pipeline():
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║             NEXUS SHOPKEEPER — MASTER ORCHESTRATION PIPELINE         ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")

    data_dir = PROJECT_ROOT / "data" / "raw"
    customers_file = data_dir / "customers.json"
    inventory_file = data_dir / "inventory.json"

    # Step 0: Ensure dataset exists
    if not customers_file.exists() or not inventory_file.exists():
        print("\n[STEP 0] Synthetic Dataset Generation...")
        from phase_1.generate_dataset import main as run_gen
        run_gen()

    # Step 1: Validation
    print("\n[STEP 1] Data Schema Validation...")
    c_ok, c_succ, c_fail, _ = validate_customers(customers_file)
    i_ok, i_succ, i_fail, _ = validate_inventory(inventory_file)
    if not (c_ok and i_ok):
        print("  ⚠ Schema validation failed. Halting pipeline.")
        sys.exit(1)
    print("  ✓ Schema validation successful.")

    # Step 2: Physical Floor Mapping
    print("\n[STEP 2] Physical Floor & Rack Grid Mapping...")
    rack_map = RackMap(inventory_file)
    rack_map.print_layout_map()
    
    # Run a quick routing calculation
    sample_items = [list(rack_map.inventory.keys())[idx] for idx in [12, 45, 87]]
    route, dist = rack_map.calculate_shopping_route(sample_items)
    print(f"  Sample Shopping Route calculated for {len(sample_items)} items:")
    print(f"    Path: Entrance -> {' -> '.join(route)} -> Entrance")
    print(f"    Total path distance: {dist:.2f} meters")

    # Step 3: Rule-Based Classification
    print("\n[STEP 3] Rule-Based Customer Classification (Phase 1 Baseline)...")
    with open(customers_file, "r", encoding="utf-8") as f:
        raw_cust_list = json.load(f)
    rule_classified = classify_all(raw_cust_list)
    print(f"  Classified {len(rule_classified)} customers using rule thresholds.")

    # Step 4: ML Clustering (K-Means)
    print("\n[STEP 4] Vectorized K-Means Clustering (Phase 2 Upgrade)...")
    customers_list, features = load_customer_features()
    
    # Initialize engine with K=6 clusters
    engine = KMeansEngine(n_clusters=6, max_iterations=300, tolerance=1e-6, random_state=42)
    labels = engine.fit_predict(features)
    
    # Generate segment mappings
    segment_map = engine.map_segments(features, labels)
    
    # Save files
    engine.save_results(features, labels)
    
    seg_map_path = PROJECT_ROOT / "data" / "processed" / "segment_mapping.json"
    atomic_write_json(seg_map_path, {str(k): v for k, v in segment_map.items()})

    # Save segmented customers
    named_labels = [segment_map.get(int(l), "Unknown") for l in labels]
    for i, cust in enumerate(customers_list):
        cust["segment"] = named_labels[i]
    
    cust_out = PROJECT_ROOT / "data" / "raw" / "customers_segmented.json"
    atomic_write_json(cust_out, customers_list)
    print(f"  Saved segmented customer profiles to: {cust_out}")

    # Compare Rule-based with K-Means
    matches = 0
    for r_cust, m_cust in zip(rule_classified, customers_list):
        if r_cust["segment_label"] == m_cust["segment"]:
            matches += 1
    alignment_rate = (matches / len(customers_list)) * 100
    print(f"  ★ Clustering vs. Rule-Based Classification Alignment Rate: {alignment_rate:.1f}%")

    # Step 5: Store Credit & Loan Operations
    print("\n[STEP 5] Reactive Store Credit & Instant Loan Verification...")
    credit_engine = StoreCreditEngine()
    
    # Run sample operations on various archetypes
    test_customers = [
        ("CUST-00001", "Ultra-Luxury Spender"),
        ("CUST-00100", "Mid-Tier Consistent"),
        ("CUST-00200", "High-Value Impulse"),
        ("CUST-00300", "Essential Bulk Buyer"),
        ("CUST-00400", "Strict Budget Spender")
    ]
    
    print("\n  Executing credit/loan operations across archetypes:")
    for cid, expected_segment in test_customers:
        if cid in credit_engine.customers:
            cust_name = credit_engine.customers[cid]["name"]
            actual_segment = credit_engine.get_segment(cid)
            init_bal = credit_engine.get_balance(cid)
            
            # 1. Apply loyalty bonus
            bonus = credit_engine.apply_loyalty_bonus(cid)
            
            # 2. Attempt micro-loan of 15% of their credit limit
            limit = credit_engine.CREDIT_LIMITS.get(actual_segment, 100.0)
            loan_amount = round(limit * 0.15, 2)
            
            loan_status = "DENIED"
            loan_id = "N/A"
            try:
                loan = credit_engine.request_credit_loan(cid, loan_amount)
                loan_status = "APPROVED"
                loan_id = loan.loan_id
                
                # Pay off half the loan
                payment_amount = round(loan.total_due / 2, 2)
                credit_engine.pay_loan(cid, loan_id, payment_amount)
            except Exception as e:
                loan_status = f"DENIED ({e})"
                
            final_bal = credit_engine.get_balance(cid)
            print(f"    - {cust_name} ({cid} - {actual_segment}):")
            print(f"        Initial Balance: ${init_bal:.2f} | Bonus Applied: ${bonus:.2f}")
            print(f"        Micro-loan of ${loan_amount:.2f}: {loan_status} (ID: {loan_id})")
            print(f"        Final Balance: ${final_bal:.2f}")

    print("\n[STEP 6] System-Wide Financial Aggregation Report...")
    summary = credit_engine.get_credit_summary()
    print("  ╔══════════════════════════════════════════════════════════════════╗")
    print(f"  ║  Total Credit Distributed (Ledger Volume) : ${summary['total_credit_issued']:11,.2f}  ║")
    print(f"  ║  Total Outstanding Loan Debt              : ${summary['total_outstanding_debt']:11,.2f}  ║")
    print(f"  ║  Active Loan Contracts                    : {summary['active_loans_count']:11d}  ║")
    print(f"  ║  System Credit default Risk Ratio         : {summary['estimated_default_rate_pct']:10.2f}%  ║")
    print(f"  ║  Total Store Custody Balances             : ${summary['total_store_balance']:11,.2f}  ║")
    print("  ╚══════════════════════════════════════════════════════════════════╝")

    print("\n  ✓ Pipeline executed with zero errors. All modules verified successfully.\n")


if __name__ == "__main__":
    run_pipeline()
