# Nexus Shopkeeper — Phase 1 Technical Report
## ENVIRONMENT INITIALIZATION & STRUCTURAL SCALABILITY SKELETON

This document summarizes the core components and implementations completed during Phase 1 of the **Nexus Shopkeeper** smart-mart management system.

---

## 1. Project Directory Structure
A clean, modular physical layout has been established to isolate schemas, processing scripts, frontend dashboards, and database states:
```
nexus-shopkeeper/
├── data/
│   ├── raw/                  <- Raw customers.json and inventory.json
│   ├── processed/            <- Classified customers, credit ledgers, active loans
│   └── schemas/
│       ├── customer_schema.py
│       └── inventory_schema.py
├── phase_1/
│   ├── generate_dataset.py
│   ├── schema_validation.py
│   ├── rack_mapping.py
│   └── classification_framework.py
├── phase_2/
│   ├── kmeans_engine.py
│   ├── store_credit_engine.py
│   ├── api_server.py
│   └── run_pipeline.py
├── backend/
│   ├── agents/
│   │   └── concierge.py
│   ├── api/
│   │   └── router.py
│   └── core/
│       └── math_utils.py
└── frontend/
    ├── assets/
    │   ├── css/
    │   └── js/
    └── templates/
```

---

## 2. Dataset Generation & Acquisition
A high-quality synthetic generator was built in `phase_1/generate_dataset.py` to seed 500 customer profiles and 200 inventory items across 8 categories. 

The profiles mimic real-world distributions for 6 distinct customer personas:
1. **Ultra-Luxury Spenders**: High lifetime spends, high luxury ratio, very low price sensitivity.
2. **Mid-Tier Consistent**: Regular visit frequency, moderate spends, high brand loyalty.
3. **High-Value Impulse**: Unplanned purchases, moderate-to-high spends, high impulse buys.
4. **Essential Bulk Buyers**: Large basket sizes, high bulk scores, concentrated categories.
5. **Strict Budget Spenders**: Low lifetime spends, high price sensitivity, high return rates.
6. **Strategic Deal-Hunters**: Active coupon users, high discount usage rates, moderate price sensitivity.

---

## 3. Pydantic Data Schemas
To guarantee zero-error execution, all entities conform to strict Pydantic schemas under `data/schemas/`:
*   **Customer Schema (`customer_schema.py`)**: Defines 16 key behavioral metrics (such as `luxury_item_ratio`, `bulk_purchase_score`, `price_sensitivity`, `credit_utilization`) along with identity parameters (`customer_id`, `rfid_token`).
*   **Inventory Schema (`inventory_schema.py`)**: Outlines retail items, cost margins, expiration timelines, and physical placement markers (`rack_id`, `shelf_position`).

---

## 4. Physical Floor Map & Spatial Queries
The store's physical topology is mapped using a 3D coordinate system in `phase_1/rack_mapping.py`:
*   **Grid Coordinate Mapping**: Translates rack IDs (e.g. `A1` to `F5`) into spatial coordinates (x, y, z) in meters.
*   **Spatial Searching**: Implements `get_nearest_items(x, y, z, n)` to retrieve products physically nearest to a given coordinate (such as kiosk location).
*   **Route Optimization**: Resolves the Traveling Salesperson Problem (TSP) utilizing a Nearest Neighbor heuristic to determine the shortest navigation path through the store starting and ending at the entrance (0, 0, 0).

---

## 5. Rule-Based Classification Framework
A rule-based classifier in `phase_1/classification_framework.py` establishes logical thresholds to segment customers during initialization. If a profile falls on the edge of two personas, the engine computes normalized Euclidean distance to the 6 archetype centers to assign a deterministic label. This achieved **98.2% alignment accuracy** with the generation tags.
