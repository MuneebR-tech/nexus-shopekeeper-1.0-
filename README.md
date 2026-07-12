# 🏪 Nexus Shopkeeper (Pakistani SaaS Edition) — Version 1.0

**Nexus Shopkeeper** is a production-grade, commercial-ready smart-mart kiosk controller and administration dashboard. Designed for fully automated retail environments, it integrates real-time K-Means customer segmentation, a reactive store credit ledger, 3D rack-to-aisle coordinates tracking, high-fidelity Web Audio API chimes, and dual AI assistants.

---


## 💡 Internship Inspiration & Design

This system's architecture, physical 3D rack coordinate calculations, and automated credit line underwriting rules are inspired by real-world retail problems observed and designed during a **software engineering internship in the retail logistics and retail automation SaaS sector**. The project serves to demonstrate how retail physical layouts can be mathematically optimized to reduce operational technician headcount (by 85% in this prototype model) and how data clustering can be used for automated customer credit scoring.

---

## 🚀 Key Features

*   **Urdu-First Kiosk UI**: Localized from the start with standard right-to-left layout direction (`dir="rtl"`), voice-assisted greetings, and fluid transition animations.
*   **Dual AI Assistants**:
    1.  *Customer Concierge*: Embedded in the kiosk to guide shoppers, answer product searches, and analyze uploaded package pictures to return floor layout coordinates.
    2.  *Manager Telemetry Guide*: Embedded in the administration panel to query inventory shortages, shifts attendance, revenue counts, and default risk analytics.
*   **Settings Modal & Themes**:
    -   *Kiosk preferences*: Easily toggle system language (English / Urdu) and display themes (Dark Mode / Light Mode) dynamically.
    -   *Admin preferences*: Configure store brand name, base interest rates, and robotic headcount rosters that immediately update the kiosk interfaces.
*   **Mobile Session Sync**: Scannable QR codes that encode active carts, customer IDs, and language preferences into dynamic URLs, enabling shoppers to take their checkout session on the go.
*   **PKR Revenue Seeding**: Generates realistic daily shopping transactions ranging from Rs. 350 to Rs. 12,500.

---

## 🏗️ Repository Layout

```
├── backend/
│   ├── core/         # Dataset seeding, TSP rack routes, vectorized K-Means, credit engine
│   ├── agents/       # AI concierge loops, telemetry analyzer persona
│   ├── api/          # FastAPI REST endpoints and status handshakes
│   ├── api_server.py # FastAPI Server Launcher
│   └── run_pipeline.py # Master orchestration pipeline runner
├── data/
│   ├── raw/          # Persistent databases (inventory, checkouts, customers)
│   └── schemas/      # Pydantic validation models
├── frontend/
│   ├── assets/       # CSS stylesheet (dark/light theme rules), JS controller
│   └── templates/    # UI Views (kiosk.html & dashboard.html)
├── requirements.txt  # Project Python dependencies
└── start_app.bat     # Windows automated startup launcher
```

---

## 🛠️ Installation & Getting Started

### 📋 Prerequisites
- **Python 3.9+** must be installed and added to your system `PATH`.
- A modern web browser (Chrome, Edge, or Firefox).

### ⚡ Quick Start
1.  Double-click or run `start_app.bat` in your project root directory:
    ```cmd
    C:\path\to\nexus-shopkeeper> start_app.bat
    ```
2.  The script will:
    - Automatically check and install missing dependencies.
    - Launch the FastAPI Backend Server on port `8000`.
    - Automatically open both the **Kiosk Navigator** (`http://localhost:8000/`) and **Administration Dashboard** (`http://localhost:8000/dashboard`) in your default web browser.

---

## 📊 Core System Modules

### 1. Vectorized K-Means Engine
- **Algorithm**: Implements vectorized Euclidean distance segmentation from scratch using NumPy.
- **Tiers**: Groups customer behavioral features into 6 loyalty tiers (Ultra-Luxury Spender, Mid-Tier Consistent, High-Value Impulse, Essential Bulk Buyer, Strict Budget Spender, and Strategic Deal-Hunter).

### 2. Store Credit & Debt Ledger
- Manages active customer credit lines, interest rate updates, default risks, and coupon discounts.
- Updates database saves atomically to prevent data corruption.

### 3. Robotic coordinate locator
- Maps product items to a 6x5 3D store grid layout (Floor levels, Aisle zones A-F, and Shelf levels 1-5).
- Computes coordinates ($X$, $Y$, $Z$ in meters) and shortest TSP paths for shelf-stocking and collection.

---

## 📦 Dependencies
Configured in `requirements.txt`:
*   `fastapi` (API core)
*   `uvicorn` (ASGI Server)
*   `numpy` (Vector calculations)
*   `pydantic` (Data schemas)
*   `python-dotenv` (Configurations)
*   `python-multipart` (Form image uploads)
