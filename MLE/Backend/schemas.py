from pydantic import BaseModel
from typing import Literal

# --- Sales Forecasting Schema ---
class SalesInput(BaseModel):
    date: str  # Format: YYYY-MM-DD
    store_nbr: int
    prod_qty: int
    txn_count: int
    sales_lag_1: float
    sales_lag_7: float
    rolling_mean_7: float

    class Config:
        json_schema_extra = {
            "example": {
                "date": "2019-06-30",
                "store_nbr": 77,
                "prod_qty": 50,
                "txn_count": 20,
                "sales_lag_1": 150.5,
                "sales_lag_7": 140.0,
                "rolling_mean_7": 145.2
            }
        }

# --- Churn Prediction Schema ---
class ChurnInput(BaseModel):
    recency: int
    frequency: int
    monetary: float
    lifestage: Literal[
        'YOUNG SINGLES/COUPLES', 'MIDAGE SINGLES/COUPLES', 'OLDER SINGLES/COUPLES',
        'YOUNG FAMILIES', 'MIDAGE FAMILIES', 'OLDER FAMILIES', 'RETIREES', 'NEW FAMILIES'
    ]
    premium_customer: Literal['Budget', 'Mainstream', 'Premium']

    class Config:
        json_schema_extra = {
            "example": {
                "recency": 10,
                "frequency": 5,
                "monetary": 25.50,
                "lifestage": "YOUNG SINGLES/COUPLES",
                "premium_customer": "Mainstream"
            }
        }
