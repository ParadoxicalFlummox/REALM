from __future__ import annotations
from typing import Optional
from decimal import Decimal
from datetime import date
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum


class Property(SQLModel, table=True):
    # The table property tells SQLModel that this class represents a real DB table
    __tablename__ = "property"
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

# The transaction models, tracks expences of a property
class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: Decimal = Field(default=0, max_digits=12, decimal_places=2)
    category: str = Field(index=True)
    transaction_type: TransactionType = Field(default=TransactionType.INCOME)
    transaction_date: date = Field(default_factory=date.today)
    description: Optional[str] = None

    property_id: int = Field(foreign_key="property.id")

# The asset model for tools, equipment, etc.
class Asset(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    purchase_price: Decimal = Field(default=0, max_digits=12, decimal_places=2)
    purchase_date: Optional[date] = None
    serial_number: Optional[str] = None
    # Allows a user to enter assets that belong to a property (like a lawnmower)
    property_id: Optional[int] = Field(default=None, foreign_key="property.id")