"""
Nexus Shopkeeper - Phase 1: Schema Validation Script
Loads customers.json and inventory.json, validates every record against the Pydantic schemas,
and reports validation results with counts and any errors.
"""

import json
import os
import sys
from pathlib import Path
from pydantic import ValidationError

# Add project root to python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from data.schemas.customer_schema import CustomerProfile
from data.schemas.inventory_schema import InventoryItem


def validate_customers(file_path: Path):
    print("------------------------------------------------------------------------")
    print(f"Validating Customers: {file_path}")
    print("------------------------------------------------------------------------")
    if not file_path.exists():
        print(f"Error: Customer file {file_path} does not exist.")
        return False, 0, 0, []

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return False, 0, 0, [str(e)]

    success_count = 0
    failure_count = 0
    errors = []

    for idx, record in enumerate(data):
        try:
            # Validate using Pydantic model
            CustomerProfile(**record)
            success_count += 1
        except ValidationError as e:
            failure_count += 1
            cust_id = record.get("customer_id", f"INDEX-{idx}")
            errors.append(f"Customer {cust_id} validation failed: {e}")

    print(f"Total Records: {len(data)}")
    print(f"Successfully Validated: {success_count}")
    print(f"Failed Validation: {failure_count}")

    if failure_count > 0:
        print("\nErrors encountered (first 5 shown):")
        for err in errors[:5]:
            print(f"  - {err}")
    else:
        print("  All customer records validated successfully!")

    return failure_count == 0, success_count, failure_count, errors


def validate_inventory(file_path: Path):
    print("\n------------------------------------------------------------------------")
    print(f"Validating Inventory: {file_path}")
    print("------------------------------------------------------------------------")
    if not file_path.exists():
        print(f"Error: Inventory file {file_path} does not exist.")
        return False, 0, 0, []

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return False, 0, 0, [str(e)]

    success_count = 0
    failure_count = 0
    errors = []

    for idx, record in enumerate(data):
        try:
            # Validate using Pydantic model
            InventoryItem(**record)
            success_count += 1
        except ValidationError as e:
            failure_count += 1
            item_id = record.get("item_id", f"INDEX-{idx}")
            errors.append(f"Inventory item {item_id} (name: {record.get('name', 'Unknown')}) validation failed: {e}")

    print(f"Total Records: {len(data)}")
    print(f"Successfully Validated: {success_count}")
    print(f"Failed Validation: {failure_count}")

    if failure_count > 0:
        print("\nErrors encountered (first 5 shown):")
        for err in errors[:5]:
            print(f"  - {err}")
    else:
        print("  All inventory records validated successfully!")

    return failure_count == 0, success_count, failure_count, errors


def main():
    customers_file = PROJECT_ROOT / "data" / "raw" / "customers.json"
    inventory_file = PROJECT_ROOT / "data" / "raw" / "inventory.json"

    print("========================================================================")
    print("  NEXUS SHOPKEEPER - Phase 1 Schema Validation Pipeline")
    print("========================================================================")

    c_ok, c_succ, c_fail, _ = validate_customers(customers_file)
    i_ok, i_succ, i_fail, _ = validate_inventory(inventory_file)

    print("\n================================ SUMMARY ===============================")
    if c_ok and i_ok:
        print("  SUCCESS: All data conforms to schemas.")
        sys.exit(0)
    else:
        print(f"  FAILURE: Validation errors found. Customers failed={c_fail}, Inventory failed={i_fail}")
        sys.exit(1)


if __name__ == "__main__":
    main()
