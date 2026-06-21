"""
Nexus Shopkeeper - Inventory Item Schema
Pydantic models for retail inventory with rack/shelf position tracking.
"""

from typing import Optional
from pydantic import BaseModel, Field, validator

VALID_CATEGORIES = [
    "beverages", "snacks", "pantry", "dairy",
    "frozen", "produce", "household", "personal_care",
]


class InventoryItem(BaseModel):
    """Single SKU record with physical placement and supply-chain metadata."""

    item_id: str = Field(..., description="Unique item identifier (e.g. SKU-0001)")
    name: str = Field(..., min_length=1, description="Product display name")
    category: str = Field(..., description="Product category")
    price: float = Field(..., gt=0, description="Retail price in USD")
    cost: float = Field(..., gt=0, description="Wholesale cost in USD")
    stock_quantity: int = Field(..., ge=0, description="Current on-hand quantity")
    rack_id: str = Field(..., description="Physical rack identifier (e.g. 'A1', 'B3')")
    shelf_position: int = Field(..., ge=1, le=5, description="Shelf level 1 (bottom) to 5 (top)")
    reorder_threshold: int = Field(..., ge=0, description="Reorder point quantity")
    supplier: str = Field(..., min_length=1, description="Supplier / distributor name")
    weight_kg: float = Field(..., gt=0, description="Item weight in kilograms")
    is_luxury: bool = Field(False, description="Whether this is a luxury/premium item")
    is_bulk_eligible: bool = Field(False, description="Whether bulk discounts are available")
    expiry_days: Optional[int] = Field(None, ge=1, description="Shelf life in days (None for non-perishable)")

    @validator("category")
    def validate_category(cls, v):
        if v not in VALID_CATEGORIES:
            raise ValueError(f"category must be one of {VALID_CATEGORIES}, got '{v}'")
        return v

    @validator("rack_id")
    def validate_rack_id(cls, v):
        if len(v) < 2 or not v[0].isalpha() or not v[1:].isdigit():
            raise ValueError(f"rack_id must be letter+digit (e.g. 'A1'), got '{v}'")
        return v

    @validator("cost")
    def cost_below_price(cls, v, values):
        if "price" in values and v >= values["price"]:
            raise ValueError("cost must be less than price")
        return v

    @property
    def margin(self) -> float:
        return self.price - self.cost

    @property
    def margin_pct(self) -> float:
        return (self.price - self.cost) / self.price * 100

    class Config:
        schema_extra = {
            "example": {
                "item_id": "SKU-0001",
                "name": "Organic Whole Milk 1L",
                "category": "dairy",
                "price": 5.49,
                "cost": 3.20,
                "stock_quantity": 48,
                "rack_id": "C2",
                "shelf_position": 3,
                "reorder_threshold": 12,
                "supplier": "Green Valley Farms",
                "weight_kg": 1.05,
                "is_luxury": False,
                "is_bulk_eligible": True,
                "expiry_days": 14,
            }
        }


if __name__ == "__main__":
    example = InventoryItem(**InventoryItem.Config.schema_extra["example"])
    print("InventoryItem schema validated OK")
    print(f"  Margin: ${example.margin:.2f} ({example.margin_pct:.1f}%)")
    print(f"  Valid categories: {VALID_CATEGORIES}")
    print(f"  Schema fields: {list(InventoryItem.__fields__.keys())}")
