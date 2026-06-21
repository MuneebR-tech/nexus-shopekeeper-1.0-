# Nexus Shopkeeper — Phase 2 Technical Report
## VECTORIZED ML K-MEANS ENGINE & REACTIVE STORE CREDIT SYSTEM

This document details the machine learning models, credit underwriting algorithms, and API server implementations delivered in Phase 2 of the **Nexus Shopkeeper** SaaS platform.

---

## 1. Vectorized K-Means Clustering Engine (`kmeans_engine.py`)
To dynamically discover and re-cluster customer behaviors as transaction data accumulates, we implemented a vectorized K-Means clustering algorithm using pure **NumPy** (without relying on external libraries like scikit-learn):

*   **Initialization (K-Means++)**: Seeding is computed using distance-weighted probabilities to ensure fast convergence and bypass local minima.
*   **Vectorization**: Pairwise distance matrices are computed utilizing NumPy broadcasting (`diff = data[:, np.newaxis, :] - centroids[np.newaxis, :, :]`), making iterations execute in milliseconds.
*   **Silhouette Scoring**: A vectorized silhouette score module evaluates the cohesion and separation of clusters, validating the quality of customer segregation.
*   **Segment Mapping**: Dynamically maps cluster centers to the 6 predefined retail archetypes by calculating normalized Euclidean distance to expected profile centers.
*   **Persistence**: Model outputs are persisted to disk as `.npy` files (`customer_features.npy`, `cluster_labels.npy`, `cluster_centroids.npy`) for low-latency retrieval.

---

## 2. Reactive Store Credit Engine (`store_credit_engine.py`)
To facilitate autonomous payments and financing within the mart kiosk, the store credit engine governs accounts reactive to customer segments:

*   **Credit Limits**: Limits scale with segment purchasing power (Ultra-Luxury Spenders = $5000, Strict Budget Spenders = $200).
*   **Instant Micro-Loans**: Customers can request loans on the fly. Approvals verify outstanding debt limits and segment eligibility.
*   **Segment-Specific Interest Rates**: Active loan principal incurs simple interest based on risk tiers (Ultra-Luxury Spenders = 0% APR, Budget Spenders = 8% APR).
*   **Loyalty Bonus**: Dynamically rewards customers with store credit multipliers depending on visit frequency and brand loyalty profiles.
*   **Persistence**: Transaction histories are stored in `data/processed/credit_ledger.json` and active contracts in `data/processed/active_loans.json`.

---

## 3. Autonomous Concierge Agent (`concierge.py`)
Leverages the **Antigravity SDK** to drive real-time personalization at checkout:
*   Imports `google.antigravity.Agent` and `LocalAgentConfig`.
*   During RFID handshakes, pulls the customer's cluster label, credit history, and name, formulating a personal prompt context.
*   Triggers tailored greetings and product recommendations matching the shopping profile (e.g. suggesting luxury wines to premium buyers or active discount coupons to budget hunters).

---

## 4. FastAPI Server & Router (`api_server.py`, `router.py`)
Exposes the business logic to the web dashboard and kiosk frontends:
*   Exposes 15+ REST endpoints across customers, inventory tracking, clustering execution, credit management, and system status.
*   Includes CORS middleware to enable multi-device kiosk operations.
*   Serves the static assets (CSS, JS, templates) of the glassmorphic dark-theme visual UI directly.
