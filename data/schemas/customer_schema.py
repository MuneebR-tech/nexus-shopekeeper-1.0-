"""
Nexus Shopkeeper - Customer Profile Schema
Pydantic models for the 16-dimensional customer feature space plus identity fields.
"""

from typing import Optional
from pydantic import BaseModel, Field, validator


class CustomerFeatures(BaseModel):
    """16-dimensional feature vector for customer behavior profiling."""

    total_spend: float = Field(..., ge=0, description="Lifetime spending total in USD")
    avg_transaction_value: float = Field(..., ge=0, description="Average per-visit spend in USD")
    visit_frequency: float = Field(..., ge=0, description="Monthly visit count")
    days_since_last_visit: int = Field(..., ge=0, description="Days since most recent visit")
    luxury_item_ratio: float = Field(..., ge=0.0, le=1.0, description="Fraction of purchases that are luxury items")
    bulk_purchase_score: float = Field(..., ge=0.0, le=1.0, description="Bulk buying tendency score")
    discount_usage_rate: float = Field(..., ge=0.0, le=1.0, description="Coupon/deal usage rate")
    impulse_buy_score: float = Field(..., ge=0.0, le=1.0, description="Unplanned purchase tendency")
    brand_loyalty_index: float = Field(..., ge=0.0, le=1.0, description="Brand stickiness index")
    price_sensitivity: float = Field(..., ge=0.0, le=1.0, description="Price influence on purchase decisions")
    category_diversity: float = Field(..., ge=0.0, le=1.0, description="Shopping breadth across categories")
    peak_hour_shopping: float = Field(..., ge=0.0, le=1.0, description="Ratio of peak vs off-peak visits")
    return_rate: float = Field(..., ge=0.0, le=1.0, description="Item return frequency")
    credit_utilization: float = Field(..., ge=0.0, le=1.0, description="Store credit usage ratio")
    seasonal_variation: float = Field(..., ge=0.0, le=1.0, description="Spending variance by season")
    engagement_score: float = Field(..., ge=0.0, le=1.0, description="Kiosk/promotion interaction score")

    def to_vector(self):
        """Return feature values as a flat list (useful for ML pipelines)."""
        return [
            self.total_spend,
            self.avg_transaction_value,
            self.visit_frequency,
            self.days_since_last_visit,
            self.luxury_item_ratio,
            self.bulk_purchase_score,
            self.discount_usage_rate,
            self.impulse_buy_score,
            self.brand_loyalty_index,
            self.price_sensitivity,
            self.category_diversity,
            self.peak_hour_shopping,
            self.return_rate,
            self.credit_utilization,
            self.seasonal_variation,
            self.engagement_score,
        ]

    @staticmethod
    def feature_names():
        return [
            "total_spend", "avg_transaction_value", "visit_frequency",
            "days_since_last_visit", "luxury_item_ratio", "bulk_purchase_score",
            "discount_usage_rate", "impulse_buy_score", "brand_loyalty_index",
            "price_sensitivity", "category_diversity", "peak_hour_shopping",
            "return_rate", "credit_utilization", "seasonal_variation",
            "engagement_score",
        ]


class CustomerProfile(BaseModel):
    """Full customer record: identity fields + 16-dim feature vector."""

    customer_id: str = Field(..., description="Unique customer identifier (e.g. CUST-00001)")
    name: str = Field(..., min_length=1, description="Customer full name")
    email: str = Field(..., description="Customer email address")
    phone: str = Field(..., description="Customer phone number")
    rfid_token: str = Field(..., description="RFID wristband / card token")
    segment_label: Optional[str] = Field(None, description="Assigned segment label (may be None before classification)")
    store_credit_balance: float = Field(0.0, ge=0.0, description="Current store credit balance in USD")
    features: CustomerFeatures = Field(..., description="16-dimensional behavioral feature vector")

    @validator("email")
    def validate_email(cls, v):
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Invalid email format")
        return v

    @validator("customer_id")
    def validate_customer_id(cls, v):
        if not v.startswith("CUST-"):
            raise ValueError("customer_id must start with 'CUST-'")
        return v

    class Config:
        schema_extra = {
            "example": {
                "customer_id": "CUST-00001",
                "name": "Alice Johnson",
                "email": "alice.johnson@email.com",
                "phone": "+1-555-0101",
                "rfid_token": "RFID-A1B2C3D4",
                "segment_label": "Ultra-Luxury Spender",
                "store_credit_balance": 125.50,
                "features": {
                    "total_spend": 28500.0,
                    "avg_transaction_value": 185.0,
                    "visit_frequency": 12.5,
                    "days_since_last_visit": 3,
                    "luxury_item_ratio": 0.72,
                    "bulk_purchase_score": 0.15,
                    "discount_usage_rate": 0.08,
                    "impulse_buy_score": 0.35,
                    "brand_loyalty_index": 0.88,
                    "price_sensitivity": 0.12,
                    "category_diversity": 0.65,
                    "peak_hour_shopping": 0.40,
                    "return_rate": 0.05,
                    "credit_utilization": 0.30,
                    "seasonal_variation": 0.45,
                    "engagement_score": 0.78,
                },
            }
        }


if __name__ == "__main__":
    # Quick smoke test
    example = CustomerProfile(**CustomerProfile.Config.schema_extra["example"])
    print("CustomerProfile schema validated OK")
    print(f"  Feature vector length: {len(example.features.to_vector())}")
    print(f"  Feature names: {CustomerFeatures.feature_names()}")
    print(f"  Schema fields: {list(CustomerProfile.__fields__.keys())}")
