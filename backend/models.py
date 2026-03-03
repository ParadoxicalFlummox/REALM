from typing import Optional
from decimal import Decimal
from datetime import date
from sqlmodel import SQLModel, Field

class Property(SQLModel, table=True):
    # The table property tells SQLModel that this class represents a real DB table
    id: Optional[int] = Field(default=None, primary_key=True)

    # The core data for the property
    nickname: str = Field(index=True) # Allows for "That One House"
    address: str

    # Financial data (force max 2 decimal points for money)
    purchase_price: Decimal = Field(default=0, max_digits=12, decimal_places=2)
    purchase_date: Optional[date] = None

    # Stats
    square_footage: Optional[int] = None
    is_active: bool = Field(default=True)
