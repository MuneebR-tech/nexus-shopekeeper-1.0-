"""
Nexus Shopkeeper - Phase 1: Synthetic Dataset Generator
Generates 500 customer profiles (6 realistic segments) and 200 inventory items (8 categories).
Uses numpy for statistically realistic distributions per segment.
"""

import json
import os
import sys
import random
import string
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_RAW.mkdir(parents=True, exist_ok=True)

# Reproducibility
np.random.seed(42)
random.seed(42)


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------
def clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return float(max(lo, min(hi, v)))


def clamp_positive(v: float) -> float:
    return float(max(0.0, v))


def make_rfid() -> str:
    return "RFID-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))


FIRST_NAMES = [
    "Aarav", "Aisha", "Akira", "Alice", "Amir", "Ana", "Benjamin", "Camila",
    "Carlos", "Charlotte", "Chen", "Chloe", "Daniel", "David", "Elena", "Emily",
    "Ethan", "Fatima", "Gabriel", "Grace", "Hannah", "Hassan", "Isabella", "Jack",
    "James", "Jasmine", "Jayden", "Julia", "Kai", "Kenji", "Layla", "Leo",
    "Liam", "Lily", "Lucas", "Luna", "Maria", "Mason", "Mateo", "Maya",
    "Mia", "Mohammed", "Nadia", "Nathan", "Noah", "Noor", "Olivia", "Omar",
    "Priya", "Rafael", "Rina", "Ryan", "Sakura", "Samuel", "Sara", "Sophia",
    "Stefan", "Tatiana", "Thomas", "Victoria", "William", "Yuki", "Zara", "Zoe",
]

LAST_NAMES = [
    "Adams", "Ali", "Anderson", "Brown", "Chang", "Chen", "Clark", "Davis",
    "Fernandez", "Garcia", "Gonzalez", "Gupta", "Hall", "Harris", "Hernandez",
    "Hill", "Ibrahim", "Jackson", "Johnson", "Jones", "Khan", "Kim", "King",
    "Kumar", "Lee", "Lewis", "Li", "Lopez", "Martin", "Martinez", "Miller",
    "Mitchell", "Moore", "Morales", "Murphy", "Nakamura", "Nelson", "Nguyen",
    "Okafor", "Patel", "Perez", "Phillips", "Ramirez", "Rivera", "Robinson",
    "Rodriguez", "Rossi", "Sanchez", "Santos", "Sato", "Schmidt", "Shah",
    "Sharma", "Singh", "Smith", "Suzuki", "Tanaka", "Taylor", "Thomas",
    "Thompson", "Torres", "Walker", "Wang", "White", "Williams", "Wilson",
    "Wright", "Wu", "Yang", "Young", "Zhang",
]

EMAIL_DOMAINS = [
    "gmail.com", "outlook.com", "yahoo.com", "protonmail.com",
    "icloud.com", "hotmail.com", "mail.com", "fastmail.com",
]


def random_name():
    return random.choice(FIRST_NAMES) + " " + random.choice(LAST_NAMES)


def random_email(name: str) -> str:
    parts = name.lower().split()
    tag = random.choice(["", str(random.randint(1, 999))])
    sep = random.choice([".", "_", ""])
    return f"{parts[0]}{sep}{parts[1]}{tag}@{random.choice(EMAIL_DOMAINS)}"


def random_phone() -> str:
    return f"+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"


# ---------------------------------------------------------------------------
# Segment-specific feature generation (the heart of the dataset)
# ---------------------------------------------------------------------------
# Each segment is a dict of (mean, std) for each feature dimension.
# We sample from truncated normal distributions and clamp to valid ranges.

SEGMENT_PROFILES = {
    "Ultra-Luxury Spender": {
        "count": 60,
        "total_spend":            (32000, 8000),
        "avg_transaction_value":  (210, 55),
        "visit_frequency":        (10, 3),
        "days_since_last_visit":  (5, 4),
        "luxury_item_ratio":      (0.72, 0.12),
        "bulk_purchase_score":    (0.15, 0.10),
        "discount_usage_rate":    (0.08, 0.06),
        "impulse_buy_score":      (0.40, 0.15),
        "brand_loyalty_index":    (0.85, 0.08),
        "price_sensitivity":      (0.10, 0.07),
        "category_diversity":     (0.65, 0.12),
        "peak_hour_shopping":     (0.35, 0.15),
        "return_rate":            (0.05, 0.03),
        "credit_utilization":     (0.25, 0.15),
        "seasonal_variation":     (0.50, 0.15),
        "engagement_score":       (0.80, 0.10),
        "store_credit_balance":   (250, 150),
    },
    "Mid-Tier Consistent": {
        "count": 175,
        "total_spend":            (9500, 3000),
        "avg_transaction_value":  (65, 20),
        "visit_frequency":        (14, 4),
        "days_since_last_visit":  (4, 3),
        "luxury_item_ratio":      (0.18, 0.10),
        "bulk_purchase_score":    (0.35, 0.15),
        "discount_usage_rate":    (0.30, 0.12),
        "impulse_buy_score":      (0.25, 0.12),
        "brand_loyalty_index":    (0.72, 0.10),
        "price_sensitivity":      (0.45, 0.12),
        "category_diversity":     (0.70, 0.10),
        "peak_hour_shopping":     (0.55, 0.15),
        "return_rate":            (0.08, 0.04),
        "credit_utilization":     (0.40, 0.15),
        "seasonal_variation":     (0.35, 0.12),
        "engagement_score":       (0.55, 0.15),
        "store_credit_balance":   (50, 40),
    },
    "High-Value Impulse": {
        "count": 90,
        "total_spend":            (14000, 5000),
        "avg_transaction_value":  (120, 40),
        "visit_frequency":        (8, 3),
        "days_since_last_visit":  (8, 5),
        "luxury_item_ratio":      (0.40, 0.15),
        "bulk_purchase_score":    (0.12, 0.08),
        "discount_usage_rate":    (0.15, 0.10),
        "impulse_buy_score":      (0.78, 0.10),
        "brand_loyalty_index":    (0.45, 0.15),
        "price_sensitivity":      (0.25, 0.12),
        "category_diversity":     (0.80, 0.10),
        "peak_hour_shopping":     (0.60, 0.15),
        "return_rate":            (0.15, 0.06),
        "credit_utilization":     (0.20, 0.12),
        "seasonal_variation":     (0.55, 0.15),
        "engagement_score":       (0.70, 0.12),
        "store_credit_balance":   (80, 60),
    },
    "Essential Bulk Buyer": {
        "count": 75,
        "total_spend":            (7500, 2500),
        "avg_transaction_value":  (95, 25),
        "visit_frequency":        (6, 2),
        "days_since_last_visit":  (12, 6),
        "luxury_item_ratio":      (0.05, 0.04),
        "bulk_purchase_score":    (0.82, 0.08),
        "discount_usage_rate":    (0.40, 0.12),
        "impulse_buy_score":      (0.10, 0.07),
        "brand_loyalty_index":    (0.60, 0.12),
        "price_sensitivity":      (0.55, 0.12),
        "category_diversity":     (0.35, 0.12),
        "peak_hour_shopping":     (0.30, 0.15),
        "return_rate":            (0.03, 0.02),
        "credit_utilization":     (0.50, 0.15),
        "seasonal_variation":     (0.20, 0.10),
        "engagement_score":       (0.35, 0.12),
        "store_credit_balance":   (30, 25),
    },
    "Strict Budget Spender": {
        "count": 50,
        "total_spend":            (2200, 800),
        "avg_transaction_value":  (22, 8),
        "visit_frequency":        (10, 4),
        "days_since_last_visit":  (6, 4),
        "luxury_item_ratio":      (0.02, 0.02),
        "bulk_purchase_score":    (0.25, 0.15),
        "discount_usage_rate":    (0.55, 0.15),
        "impulse_buy_score":      (0.08, 0.05),
        "brand_loyalty_index":    (0.50, 0.15),
        "price_sensitivity":      (0.88, 0.07),
        "category_diversity":     (0.40, 0.12),
        "peak_hour_shopping":     (0.45, 0.15),
        "return_rate":            (0.12, 0.05),
        "credit_utilization":     (0.65, 0.15),
        "seasonal_variation":     (0.30, 0.12),
        "engagement_score":       (0.25, 0.12),
        "store_credit_balance":   (10, 10),
    },
    "Strategic Deal-Hunter": {
        "count": 50,
        "total_spend":            (6500, 2500),
        "avg_transaction_value":  (55, 18),
        "visit_frequency":        (12, 4),
        "days_since_last_visit":  (5, 3),
        "luxury_item_ratio":      (0.22, 0.12),
        "bulk_purchase_score":    (0.45, 0.15),
        "discount_usage_rate":    (0.85, 0.07),
        "impulse_buy_score":      (0.30, 0.12),
        "brand_loyalty_index":    (0.38, 0.12),
        "price_sensitivity":      (0.72, 0.10),
        "category_diversity":     (0.75, 0.10),
        "peak_hour_shopping":     (0.50, 0.15),
        "return_rate":            (0.10, 0.05),
        "credit_utilization":     (0.55, 0.15),
        "seasonal_variation":     (0.60, 0.12),
        "engagement_score":       (0.72, 0.10),
        "store_credit_balance":   (40, 30),
    },
}


def generate_customer(cid: int, segment: str, profile: dict) -> dict:
    """Generate a single customer record from segment statistical profile."""
    name = random_name()

    def sample_normal(key):
        mean, std = profile[key]
        return np.random.normal(mean, std)

    features = {
        "total_spend":            round(clamp_positive(sample_normal("total_spend")), 2),
        "avg_transaction_value":  round(clamp_positive(sample_normal("avg_transaction_value")), 2),
        "visit_frequency":        round(clamp_positive(sample_normal("visit_frequency")), 1),
        "days_since_last_visit":  max(0, int(round(sample_normal("days_since_last_visit")))),
        "luxury_item_ratio":      round(clamp(sample_normal("luxury_item_ratio")), 4),
        "bulk_purchase_score":    round(clamp(sample_normal("bulk_purchase_score")), 4),
        "discount_usage_rate":    round(clamp(sample_normal("discount_usage_rate")), 4),
        "impulse_buy_score":      round(clamp(sample_normal("impulse_buy_score")), 4),
        "brand_loyalty_index":    round(clamp(sample_normal("brand_loyalty_index")), 4),
        "price_sensitivity":      round(clamp(sample_normal("price_sensitivity")), 4),
        "category_diversity":     round(clamp(sample_normal("category_diversity")), 4),
        "peak_hour_shopping":     round(clamp(sample_normal("peak_hour_shopping")), 4),
        "return_rate":            round(clamp(sample_normal("return_rate")), 4),
        "credit_utilization":     round(clamp(sample_normal("credit_utilization")), 4),
        "seasonal_variation":     round(clamp(sample_normal("seasonal_variation")), 4),
        "engagement_score":       round(clamp(sample_normal("engagement_score")), 4),
    }

    return {
        "customer_id": f"CUST-{cid:05d}",
        "name": name,
        "email": random_email(name),
        "phone": random_phone(),
        "rfid_token": make_rfid(),
        "segment_label": segment,
        "store_credit_balance": round(clamp_positive(sample_normal("store_credit_balance")), 2),
        "features": features,
    }


# ---------------------------------------------------------------------------
# Inventory generation
# ---------------------------------------------------------------------------

CATEGORY_ITEMS = {
    "beverages": [
        ("Spring Water 1L", 1.29, 0.45, 0.8, None, False, False),
        ("Sparkling Water 750ml", 2.49, 1.10, 0.75, None, False, True),
        ("Orange Juice 1L", 4.99, 2.80, 1.05, 21, False, True),
        ("Cold-Pressed Green Juice", 8.99, 4.50, 0.5, 7, True, False),
        ("Craft Root Beer 6pk", 9.99, 5.20, 2.4, None, False, True),
        ("Organic Kombucha 16oz", 4.49, 2.20, 0.48, 60, False, False),
        ("Coconut Water 330ml", 3.29, 1.60, 0.35, 180, False, True),
        ("Artisan Cold Brew Coffee", 6.99, 3.20, 0.35, 30, True, False),
        ("Energy Drink 4pk", 7.99, 4.10, 1.6, 365, False, True),
        ("Sparkling Lemonade 750ml", 3.99, 1.80, 0.8, None, False, True),
        ("Protein Shake Vanilla", 4.29, 2.30, 0.35, 180, False, True),
        ("Almond Milk 1L", 4.49, 2.40, 1.05, 60, False, True),
        ("Oat Milk Barista Blend", 5.49, 2.80, 1.0, 90, False, True),
        ("Matcha Latte Ready-to-Drink", 5.99, 2.80, 0.35, 90, True, False),
        ("Elderflower Tonic Water", 3.49, 1.60, 0.5, None, False, True),
        ("Premium Mineral Water 1L", 4.99, 2.00, 1.05, None, True, False),
        ("Iced Tea Peach 500ml", 2.99, 1.30, 0.52, 180, False, True),
        ("Ginger Beer 4pk", 6.49, 3.20, 1.6, None, False, True),
        ("Probiotic Berry Smoothie", 5.49, 2.80, 0.35, 14, False, False),
        ("Alkaline Water 1.5L", 3.79, 1.50, 1.55, None, False, True),
        ("Hibiscus Iced Tea 1L", 4.29, 2.00, 1.05, 30, False, False),
        ("Vitamin Water Citrus", 2.49, 1.10, 0.55, 270, False, True),
        ("Coconut Milk 400ml", 2.99, 1.40, 0.42, 365, False, True),
        ("Sparkling Rose Water", 3.99, 1.80, 0.35, None, True, False),
        ("Classic Lemonade 2L", 3.49, 1.50, 2.1, 14, False, True),
    ],
    "snacks": [
        ("Organic Tortilla Chips 300g", 4.49, 2.20, 0.3, 180, False, True),
        ("Dark Chocolate Bar 85%", 5.99, 2.80, 0.1, 365, True, False),
        ("Mixed Nuts 500g", 12.99, 7.50, 0.5, 180, False, True),
        ("Rice Crackers Wasabi", 3.99, 1.80, 0.15, 270, False, False),
        ("Protein Bar Variety 12pk", 24.99, 14.00, 0.72, 365, False, True),
        ("Gourmet Popcorn Truffle", 6.99, 3.20, 0.18, 120, True, False),
        ("Trail Mix Energy Blend", 7.49, 3.80, 0.4, 180, False, True),
        ("Pretzel Thins Sea Salt", 3.49, 1.60, 0.2, 270, False, True),
        ("Dried Mango Slices 200g", 5.49, 2.80, 0.2, 180, False, False),
        ("Seaweed Snack 6pk", 4.99, 2.40, 0.06, 365, False, True),
        ("Artisan Cheese Crackers", 5.99, 2.80, 0.2, 180, False, False),
        ("Veggie Chips Beetroot", 4.29, 2.10, 0.15, 120, False, True),
        ("Granola Bites Honey", 4.99, 2.40, 0.25, 180, False, True),
        ("Peanut Butter Pretzels", 4.49, 2.20, 0.35, 270, False, True),
        ("Chocolate Covered Almonds", 8.99, 4.50, 0.3, 180, True, False),
        ("Kale Chips Original", 5.49, 2.80, 0.05, 90, False, False),
        ("Fruit Leather Strips 10pk", 6.49, 3.20, 0.15, 365, False, True),
        ("Spicy Cashews 400g", 9.99, 5.20, 0.4, 180, False, True),
        ("Mini Rice Cakes 12pk", 3.79, 1.80, 0.18, 270, False, True),
        ("Belgian Chocolate Truffles", 14.99, 7.50, 0.2, 180, True, False),
        ("Plantain Chips 200g", 3.49, 1.60, 0.2, 180, False, True),
        ("Macadamia Nut Mix 300g", 11.99, 6.50, 0.3, 120, True, False),
        ("Yogurt Covered Raisins", 4.99, 2.40, 0.3, 180, False, True),
        ("Sesame Sticks 250g", 3.29, 1.50, 0.25, 270, False, True),
        ("Coconut Chips Toasted", 4.49, 2.10, 0.1, 180, False, False),
    ],
    "pantry": [
        ("Extra Virgin Olive Oil 750ml", 12.99, 7.00, 0.82, 730, False, False),
        ("Basmati Rice 2kg", 8.49, 4.50, 2.0, 730, False, True),
        ("Organic Pasta Penne 500g", 3.49, 1.60, 0.5, 730, False, True),
        ("Canned Black Beans 400g", 1.79, 0.80, 0.42, 1095, False, True),
        ("Coconut Flour 500g", 6.99, 3.50, 0.5, 365, False, False),
        ("Truffle Infused Olive Oil", 24.99, 12.00, 0.28, 365, True, False),
        ("Quinoa 1kg", 9.99, 5.20, 1.0, 730, False, True),
        ("Honey Raw Organic 500g", 11.99, 6.00, 0.55, 1095, False, False),
        ("Soy Sauce Naturally Brewed", 4.49, 2.00, 0.35, 730, False, False),
        ("Balsamic Vinegar Aged", 8.99, 4.20, 0.28, 1095, False, False),
        ("Coconut Oil Virgin 500ml", 7.49, 3.80, 0.52, 730, False, False),
        ("Canned Diced Tomatoes 800g", 2.49, 1.10, 0.85, 730, False, True),
        ("Peanut Butter Natural 400g", 5.49, 2.80, 0.42, 365, False, True),
        ("Maple Syrup Grade A 375ml", 13.99, 7.20, 0.42, 730, True, False),
        ("Sea Salt Flakes 250g", 4.99, 2.20, 0.25, None, False, False),
        ("Whole Wheat Flour 2kg", 4.49, 2.00, 2.0, 365, False, True),
        ("Arborio Risotto Rice 1kg", 6.99, 3.50, 1.0, 730, False, False),
        ("Tahini Paste 300g", 5.99, 2.80, 0.32, 365, False, False),
        ("Dried Red Lentils 1kg", 4.99, 2.40, 1.0, 730, False, True),
        ("Premium Saffron 1g", 14.99, 8.50, 0.01, 730, True, False),
        ("Apple Cider Vinegar 500ml", 4.99, 2.20, 0.52, 730, False, False),
        ("Chickpea Flour 500g", 3.99, 1.80, 0.5, 365, False, True),
        ("Almond Butter 350g", 9.99, 5.00, 0.38, 270, False, False),
        ("Panko Breadcrumbs 200g", 2.99, 1.30, 0.2, 365, False, True),
        ("Black Pepper Whole 100g", 5.49, 2.50, 0.1, 1095, False, False),
    ],
    "dairy": [
        ("Organic Whole Milk 1L", 5.49, 3.20, 1.05, 14, False, True),
        ("Greek Yogurt Plain 500g", 4.99, 2.60, 0.52, 21, False, True),
        ("Aged Cheddar Block 400g", 8.99, 4.80, 0.4, 90, False, False),
        ("Cream Cheese 250g", 3.49, 1.80, 0.26, 30, False, True),
        ("Grass-Fed Butter 250g", 5.99, 3.20, 0.26, 90, False, True),
        ("Artisan Gouda 200g", 9.99, 5.20, 0.2, 60, True, False),
        ("Cottage Cheese 400g", 4.29, 2.20, 0.42, 14, False, True),
        ("Heavy Cream 500ml", 4.49, 2.40, 0.52, 14, False, False),
        ("Mozzarella Fresh 250g", 5.99, 3.00, 0.26, 10, False, False),
        ("Parmesan Reggiano 200g", 12.99, 7.00, 0.2, 365, True, False),
        ("Skyr Icelandic Yogurt", 5.49, 2.80, 0.4, 28, False, False),
        ("Goat Cheese Log 150g", 7.99, 4.00, 0.16, 30, True, False),
        ("Sour Cream 300ml", 2.99, 1.40, 0.32, 21, False, True),
        ("Brie Wheel 200g", 8.49, 4.20, 0.2, 28, True, False),
        ("Whipped Cream Cheese", 3.99, 1.80, 0.2, 30, False, False),
        ("A2 Whole Milk 1L", 6.49, 3.50, 1.05, 14, False, True),
        ("Ricotta Cheese 450g", 5.49, 2.80, 0.47, 14, False, False),
        ("Kefir Plain 1L", 5.99, 3.00, 1.05, 21, False, False),
        ("Mascarpone 250g", 6.49, 3.20, 0.26, 14, True, False),
        ("Smoked Gouda 200g", 8.99, 4.50, 0.2, 90, True, False),
        ("Vanilla Greek Yogurt 4pk", 6.99, 3.50, 0.6, 21, False, True),
        ("Clotted Cream 200g", 7.49, 3.80, 0.22, 14, True, False),
        ("Halloumi 250g", 6.99, 3.50, 0.26, 60, False, False),
        ("Unsalted Butter 500g", 7.99, 4.20, 0.5, 90, False, True),
        ("Low-Fat Milk 2L", 4.49, 2.40, 2.05, 10, False, True),
    ],
    "frozen": [
        ("Mixed Berries 1kg", 8.99, 4.80, 1.0, 365, False, True),
        ("Veggie Stir-Fry Mix 750g", 5.49, 2.80, 0.75, 365, False, True),
        ("Premium Ice Cream Vanilla", 7.99, 3.80, 0.5, 365, False, False),
        ("Frozen Pizza Margherita", 6.49, 3.20, 0.45, 180, False, True),
        ("Edamame Shelled 500g", 4.99, 2.40, 0.5, 365, False, True),
        ("Artisan Gelato Pistachio", 12.99, 6.50, 0.5, 365, True, False),
        ("Fish Fillets Wild-Caught 4pk", 14.99, 8.00, 0.6, 365, False, True),
        ("Cauliflower Rice 500g", 4.49, 2.20, 0.5, 365, False, True),
        ("Frozen Croissants 6pk", 8.49, 4.20, 0.42, 180, False, True),
        ("Wagyu Beef Burgers 4pk", 22.99, 12.00, 0.6, 180, True, False),
        ("Frozen Acai Smoothie Packs", 9.99, 5.00, 0.4, 365, False, True),
        ("Spinach Ravioli 500g", 5.99, 2.80, 0.5, 180, False, True),
        ("Mango Chunks 750g", 6.99, 3.50, 0.75, 365, False, True),
        ("Frozen Waffles 8pk", 4.99, 2.40, 0.35, 270, False, True),
        ("Thai Green Curry Meal", 7.49, 3.80, 0.4, 180, False, False),
        ("Frozen Avocado Halves 6pk", 8.99, 4.50, 0.5, 365, False, True),
        ("Chicken Tenders Organic 500g", 9.99, 5.20, 0.52, 270, False, True),
        ("Frozen Blueberries 500g", 5.99, 3.00, 0.5, 365, False, True),
        ("Lobster Tails 2pk", 29.99, 16.00, 0.35, 180, True, False),
        ("Vegan Nuggets 400g", 6.49, 3.20, 0.4, 270, False, True),
        ("Frozen Dumplings 20pk", 7.99, 4.00, 0.5, 365, False, True),
        ("Sorbet Raspberry 500ml", 6.49, 3.20, 0.5, 365, False, False),
        ("Frozen Broccoli Florets 1kg", 4.49, 2.20, 1.0, 365, False, True),
        ("Premium Puff Pastry Sheets", 5.99, 2.80, 0.5, 180, False, False),
        ("Frozen Shrimp Large 500g", 16.99, 9.00, 0.52, 365, False, True),
    ],
    "produce": [
        ("Organic Bananas 1kg", 2.99, 1.40, 1.0, 7, False, True),
        ("Avocados Hass 4pk", 5.99, 3.20, 0.8, 5, False, True),
        ("Baby Spinach 200g", 3.99, 2.00, 0.2, 5, False, False),
        ("Roma Tomatoes 1kg", 4.49, 2.20, 1.0, 7, False, True),
        ("Blueberries 250g", 5.49, 2.80, 0.25, 7, False, False),
        ("Organic Kale Bunch", 3.49, 1.80, 0.3, 5, False, False),
        ("Sweet Potatoes 1kg", 3.99, 1.80, 1.0, 14, False, True),
        ("Red Bell Peppers 3pk", 4.99, 2.40, 0.6, 10, False, True),
        ("Fuji Apples 1kg", 4.49, 2.20, 1.0, 14, False, True),
        ("Fresh Herbs Basil Pack", 2.99, 1.40, 0.03, 5, False, False),
        ("Dragon Fruit 2pk", 8.99, 4.80, 0.7, 5, True, False),
        ("Organic Lemons 6pk", 4.49, 2.20, 0.6, 14, False, True),
        ("Cremini Mushrooms 250g", 3.99, 2.00, 0.25, 7, False, False),
        ("English Cucumber", 1.99, 0.90, 0.4, 7, False, True),
        ("Mixed Salad Greens 300g", 4.99, 2.40, 0.3, 5, False, False),
        ("Heirloom Tomatoes 500g", 6.99, 3.50, 0.5, 5, True, False),
        ("Broccoli Crown", 2.49, 1.20, 0.5, 7, False, True),
        ("Fresh Ginger Root 200g", 2.99, 1.40, 0.2, 21, False, False),
        ("Organic Strawberries 400g", 6.99, 3.50, 0.4, 5, False, False),
        ("Garlic 3-Head Pack", 2.49, 1.10, 0.15, 30, False, True),
        ("Seedless Grapes 500g", 4.99, 2.40, 0.5, 7, False, False),
        ("Zucchini 3pk", 3.49, 1.60, 0.6, 7, False, True),
        ("Mango 2pk", 4.99, 2.40, 0.7, 5, False, False),
        ("Artichokes 2pk", 5.99, 3.00, 0.6, 7, False, False),
        ("Fresh Corn 4-Ear Pack", 3.99, 1.80, 1.2, 5, False, True),
    ],
    "household": [
        ("Eco Dish Soap 750ml", 4.99, 2.40, 0.8, None, False, True),
        ("Bamboo Paper Towels 6pk", 8.99, 4.50, 1.2, None, False, True),
        ("All-Purpose Cleaner 1L", 5.49, 2.80, 1.05, None, False, True),
        ("Trash Bags 30-Count", 6.99, 3.50, 0.8, None, False, True),
        ("Laundry Pods 42ct", 14.99, 7.50, 1.2, None, False, True),
        ("Premium Soy Candle Lavender", 24.99, 11.00, 0.4, None, True, False),
        ("Sponge Set 5pk", 3.49, 1.60, 0.15, None, False, True),
        ("Glass Cleaner 750ml", 4.49, 2.20, 0.8, None, False, True),
        ("Aluminum Foil 100ft", 5.99, 2.80, 0.45, None, False, True),
        ("Parchment Paper Roll", 4.49, 2.00, 0.2, None, False, True),
        ("Food Storage Bags Gallon 50ct", 5.99, 2.80, 0.3, None, False, True),
        ("Toilet Bowl Cleaner", 3.99, 1.80, 0.7, None, False, True),
        ("Bamboo Cutting Board", 19.99, 9.50, 0.8, None, False, False),
        ("Stainless Steel Scrubbers 3pk", 4.49, 2.00, 0.1, None, False, True),
        ("Linen Spray Eucalyptus", 9.99, 4.80, 0.3, None, True, False),
        ("Reusable Produce Bags 8pk", 12.99, 6.00, 0.2, None, False, False),
        ("Floor Cleaner Concentrate", 7.49, 3.50, 0.55, None, False, True),
        ("Beeswax Food Wraps 3pk", 14.99, 7.00, 0.1, None, True, False),
        ("Microfiber Cloths 10pk", 8.99, 4.20, 0.25, None, False, True),
        ("Hand Soap Refill 1L", 6.49, 3.00, 1.05, None, False, True),
        ("Dish Drying Rack Bamboo", 29.99, 14.00, 1.5, None, True, False),
        ("Compostable Trash Bags 25ct", 7.99, 3.80, 0.4, None, False, True),
        ("Multi-Surface Wipes 80ct", 5.49, 2.60, 0.5, None, False, True),
        ("Silicone Baking Mat Set", 16.99, 8.00, 0.3, None, False, False),
        ("LED Light Bulbs 4pk", 9.99, 5.00, 0.2, None, False, True),
    ],
    "personal_care": [
        ("Natural Shampoo 400ml", 8.99, 4.20, 0.42, None, False, False),
        ("Charcoal Toothpaste 120g", 5.99, 2.80, 0.14, None, False, False),
        ("Organic Lip Balm 3pk", 7.49, 3.50, 0.03, None, False, True),
        ("Aloe Vera Body Lotion 500ml", 9.99, 4.80, 0.55, None, False, False),
        ("Bamboo Toothbrush 4pk", 6.99, 3.20, 0.08, None, False, True),
        ("Luxury Face Serum 30ml", 34.99, 15.00, 0.05, None, True, False),
        ("Deodorant Natural Stone", 8.49, 4.00, 0.08, None, False, False),
        ("Sunscreen SPF50 200ml", 12.99, 6.50, 0.22, None, False, False),
        ("Conditioner Argan Oil 400ml", 9.49, 4.50, 0.42, None, False, False),
        ("Hand Cream Shea Butter 100ml", 6.99, 3.20, 0.12, None, False, False),
        ("Facial Cleanser Foam 150ml", 11.99, 5.50, 0.18, None, False, False),
        ("Bath Bombs Gift Set 6pk", 18.99, 8.50, 0.6, None, True, False),
        ("Dental Floss Eco 3pk", 5.49, 2.60, 0.05, None, False, True),
        ("Hair Oil Treatment 100ml", 14.99, 7.00, 0.12, None, True, False),
        ("Body Wash Citrus 500ml", 7.99, 3.80, 0.55, None, False, True),
        ("Eye Cream Anti-Aging 15ml", 29.99, 13.00, 0.03, None, True, False),
        ("Razor Refill Cartridges 8pk", 19.99, 10.00, 0.1, None, False, True),
        ("Micellar Water 400ml", 8.99, 4.20, 0.42, None, False, False),
        ("Night Cream Retinol 50ml", 24.99, 11.00, 0.08, None, True, False),
        ("Cotton Rounds 100ct", 3.99, 1.80, 0.15, None, False, True),
        ("Beard Oil Cedar 30ml", 12.99, 6.00, 0.05, None, True, False),
        ("Dry Shampoo Spray 200ml", 7.49, 3.50, 0.22, None, False, False),
        ("Vitamin E Moisturizer 200ml", 10.99, 5.00, 0.22, None, False, False),
        ("Leave-In Conditioner 250ml", 9.99, 4.80, 0.28, None, False, False),
        ("Exfoliating Scrub 200g", 11.49, 5.50, 0.22, None, False, False),
    ],
}

# Rack assignment: each category gets allocated racks from a 6x5 grid (A1..F5)
RACK_ROWS = list("ABCDEF")
RACK_COLS = list(range(1, 6))
ALL_RACKS = [f"{r}{c}" for r in RACK_ROWS for c in RACK_COLS]  # 30 racks total

# Map categories to rack ranges (each category gets 3-4 racks)
CATEGORY_RACK_MAP = {
    "beverages":      ["A1", "A2", "A3"],
    "snacks":         ["A4", "A5", "B1"],
    "pantry":         ["B2", "B3", "B4", "B5"],
    "dairy":          ["C1", "C2", "C3"],
    "frozen":         ["C4", "C5", "D1"],
    "produce":        ["D2", "D3", "D4"],
    "household":      ["D5", "E1", "E2", "E3"],
    "personal_care":  ["E4", "E5", "F1", "F2"],
}

SUPPLIERS = {
    "beverages":     ["Cascade Springs", "GreenLeaf Beverages", "Pacific Drinks Co."],
    "snacks":        ["CrunchWorks", "NutHarvest Inc.", "Artisan Bites Co."],
    "pantry":        ["Global Pantry Supply", "Heritage Foods", "Mediterranean Imports"],
    "dairy":         ["Green Valley Farms", "Alpine Creamery", "Sunrise Dairy"],
    "frozen":        ["FrostPack Foods", "IceField Premium", "DeepFreeze Supply"],
    "produce":       ["Morning Harvest", "Organic Fields Direct", "Valley Fresh Farms"],
    "household":     ["CleanCo Supply", "EcoHome Goods", "BrightLife Products"],
    "personal_care": ["Pure Glow Labs", "NatureSkin Co.", "Wellness Essentials"],
}


def generate_inventory() -> list:
    """Generate 200 inventory items distributed across categories."""
    items = []
    item_counter = 0

    for category, product_list in CATEGORY_ITEMS.items():
        racks_for_cat = CATEGORY_RACK_MAP[category]
        suppliers_for_cat = SUPPLIERS[category]

        for idx, (name, price, cost, weight, expiry, is_lux, is_bulk) in enumerate(product_list):
            item_counter += 1
            rack = racks_for_cat[idx % len(racks_for_cat)]
            shelf = (idx % 5) + 1
            stock = int(np.random.lognormal(mean=3.5, sigma=0.6))
            stock = max(5, min(stock, 300))
            reorder = max(3, stock // 4)

            items.append({
                "item_id": f"SKU-{item_counter:04d}",
                "name": name,
                "category": category,
                "price": price,
                "cost": cost,
                "stock_quantity": stock,
                "rack_id": rack,
                "shelf_position": shelf,
                "reorder_threshold": reorder,
                "supplier": random.choice(suppliers_for_cat),
                "weight_kg": weight,
                "is_luxury": is_lux,
                "is_bulk_eligible": is_bulk,
                "expiry_days": expiry,
            })

    return items


# ---------------------------------------------------------------------------
# Main: generate everything and print stats
# ---------------------------------------------------------------------------
def main():
    print("=" * 72)
    print("  NEXUS SHOPKEEPER - Phase 1 Dataset Generator")
    print("=" * 72)

    # ---- Customers ----
    customers = []
    cid = 0
    for segment, profile in SEGMENT_PROFILES.items():
        count = profile["count"]
        for _ in range(count):
            cid += 1
            customers.append(generate_customer(cid, segment, profile))

    # Shuffle so segments are interleaved
    random.shuffle(customers)

    # ---- Inventory ----
    inventory = generate_inventory()

    # ---- Save ----
    customers_path = DATA_RAW / "customers.json"
    inventory_path = DATA_RAW / "inventory.json"

    with open(customers_path, "w", encoding="utf-8") as f:
        json.dump(customers, f, indent=2, ensure_ascii=False)

    with open(inventory_path, "w", encoding="utf-8") as f:
        json.dump(inventory, f, indent=2, ensure_ascii=False)

    # ---- Summary Statistics ----
    print(f"\n{'CUSTOMERS':=^72}")
    print(f"  Total generated: {len(customers)}")
    print(f"  Saved to: {customers_path}")
    print(f"\n  Segment distribution:")
    from collections import Counter
    seg_counts = Counter(c["segment_label"] for c in customers)
    for seg, cnt in sorted(seg_counts.items(), key=lambda x: -x[1]):
        print(f"    {seg:<30s} {cnt:>4d}  ({cnt/len(customers)*100:.1f}%)")

    # Feature stats per segment
    feature_keys = list(customers[0]["features"].keys())
    print(f"\n  Feature summary (global means):")
    for fk in feature_keys:
        vals = [c["features"][fk] for c in customers]
        print(f"    {fk:<28s}  mean={np.mean(vals):>10.2f}  std={np.std(vals):>8.2f}  "
              f"min={np.min(vals):>8.2f}  max={np.max(vals):>8.2f}")

    print(f"\n{'INVENTORY':=^72}")
    print(f"  Total items: {len(inventory)}")
    print(f"  Saved to: {inventory_path}")
    cat_counts = Counter(i["category"] for i in inventory)
    print(f"\n  Category distribution:")
    for cat, cnt in sorted(cat_counts.items()):
        cat_items = [i for i in inventory if i["category"] == cat]
        avg_price = np.mean([i["price"] for i in cat_items])
        avg_stock = np.mean([i["stock_quantity"] for i in cat_items])
        luxury_ct = sum(1 for i in cat_items if i["is_luxury"])
        print(f"    {cat:<16s} {cnt:>3d} items  avg_price=${avg_price:>6.2f}  "
              f"avg_stock={avg_stock:>5.0f}  luxury={luxury_ct}")

    total_value = sum(i["price"] * i["stock_quantity"] for i in inventory)
    total_luxury = sum(1 for i in inventory if i["is_luxury"])
    total_bulk = sum(1 for i in inventory if i["is_bulk_eligible"])
    print(f"\n  Total inventory value: ${total_value:,.2f}")
    print(f"  Luxury items: {total_luxury}")
    print(f"  Bulk-eligible items: {total_bulk}")
    print(f"\n{'DONE':=^72}")


if __name__ == "__main__":
    main()
