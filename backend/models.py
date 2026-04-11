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
    estimated_value: Optional[Decimal] = Field(default=None, max_digits=12, decimal_places=2)

# The transaction models, tracks expenses of a property
class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

# Schedule E tax categories (IRS standard for rental property reporting)
SCHEDULE_E_CATEGORIES = [
    "advertising",
    "auto_and_travel",
    "cleaning",
    "commissions",
    "insurance",
    "legal_and_professional",
    "management_fees",
    "mortgage_interest",
    "other_interest",
    "repairs",
    "supplies",
    "taxes",
    "utilities",
    "depreciation",
    "other",
]

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: Decimal = Field(default=0, max_digits=12, decimal_places=2)
    category: str = Field(index=True)
    # Optional Schedule E tax category for annual tax reporting
    tax_category: Optional[str] = Field(default=None, index=True)
    transaction_type: TransactionType = Field(default=TransactionType.INCOME)
    transaction_date: date = Field(default_factory=date.today)
    description: Optional[str] = None

    property_id: int = Field(foreign_key="property.id")

# The asset model for tools, equipment, etc.
class Asset(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    category: Optional[str] = Field(default=None, index=True)
    description: Optional[str] = None
    purchase_price: Decimal = Field(default=0, max_digits=12, decimal_places=2)
    purchase_date: Optional[date] = None
    serial_number: Optional[str] = None
    # Allows a user to enter assets that belong to a property (like a lawnmower)
    property_id: Optional[int] = Field(default=None, foreign_key="property.id")

# Deal analyzer snapshot — stores both inputs and computed outputs
class Deal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = None                  # user label e.g. "123 Oak — 20% down"
    address: str                                 # free text, supports pre-purchase deals
    created_at: date = Field(default_factory=date.today)
    property_id: Optional[int] = Field(default=None, foreign_key="property.id")

    # Purchase
    purchase_price: Decimal = Field(max_digits=12, decimal_places=2)
    down_payment: Decimal = Field(max_digits=12, decimal_places=2)
    closing_costs: Decimal = Field(default=Decimal("0"), max_digits=12, decimal_places=2)
    rehab_cost: Decimal = Field(default=Decimal("0"), max_digits=12, decimal_places=2)

    # Loan
    interest_rate: Decimal = Field(max_digits=5, decimal_places=3)  # e.g. 6.750
    loan_term_years: int = Field(default=30)

    # Monthly income / expenses
    monthly_rent: Decimal = Field(max_digits=12, decimal_places=2)
    vacancy_rate: Decimal = Field(default=Decimal("5.0"), max_digits=5, decimal_places=2)  # %
    monthly_property_tax: Decimal = Field(default=Decimal("0"), max_digits=12, decimal_places=2)
    insurance: Decimal = Field(default=Decimal("0"), max_digits=12, decimal_places=2)
    hoa: Decimal = Field(default=Decimal("0"), max_digits=12, decimal_places=2)
    maintenance: Decimal = Field(default=Decimal("0"), max_digits=12, decimal_places=2)
    capex: Decimal = Field(default=Decimal("0"), max_digits=12, decimal_places=2)
    utilities: Decimal = Field(default=Decimal("0"), max_digits=12, decimal_places=2)
    lawn_snow: Decimal = Field(default=Decimal("0"), max_digits=12, decimal_places=2)

    # Computed outputs — frozen at save time
    monthly_mortgage: Decimal = Field(default=Decimal("0"), max_digits=12, decimal_places=2)
    monthly_noi: Decimal = Field(default=Decimal("0"), max_digits=12, decimal_places=2)
    monthly_cash_flow: Decimal = Field(default=Decimal("0"), max_digits=12, decimal_places=2)
    annual_cash_flow: Decimal = Field(default=Decimal("0"), max_digits=12, decimal_places=2)
    annual_property_tax: Decimal = Field(default=Decimal("0"), max_digits=12, decimal_places=2)
    cash_on_cash_return: Decimal = Field(default=Decimal("0"), max_digits=7, decimal_places=4)  # %
    dscr: Decimal = Field(default=Decimal("0"), max_digits=7, decimal_places=4)
    break_even_occupancy: Decimal = Field(default=Decimal("0"), max_digits=7, decimal_places=4)  # %

# Maintenance record — tracks work done on a property or specific asset
MAINTENANCE_CATEGORIES = [
    "repair",
    "inspection",
    "cleaning",
    "landscaping",
    "hvac",
    "plumbing",
    "electrical",
    "appliance",
    "pest_control",
    "capital_improvement",
    "other",
]

class MaintenanceRecord(SQLModel, table=True):
    __tablename__ = "maintenancerecord"
    id: Optional[int] = Field(default=None, primary_key=True)
    property_id: int = Field(foreign_key="property.id")
    asset_id: Optional[int] = Field(default=None, foreign_key="asset.id")  # optional link to a specific asset

    service_date: date = Field(default_factory=date.today)
    category: str = Field(index=True)
    description: str                        # what was done
    vendor: Optional[str] = None            # who did the work
    cost: Decimal = Field(default=Decimal("0"), max_digits=12, decimal_places=2)
    warranty_expires: Optional[date] = None # optional warranty expiration
    notes: Optional[str] = None


# --- Foundation models (schema only — UI in a future release) ---

# Reminder — scheduled alerts for lease renewals, inspections, filter changes, etc.
class Reminder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    property_id: int = Field(foreign_key="property.id")
    asset_id: Optional[int] = Field(default=None, foreign_key="asset.id")
    maintenance_record_id: Optional[int] = Field(default=None, foreign_key="maintenancerecord.id")

    title: str
    due_date: date
    notes: Optional[str] = None
    is_complete: bool = Field(default=False)


# Document — file metadata for lease agreements, warranties, inspection reports, etc.
# Actual file storage is out of scope for v1.0 (filesystem or S3 in a future release)
class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    property_id: int = Field(foreign_key="property.id")
    asset_id: Optional[int] = Field(default=None, foreign_key="asset.id")
    maintenance_record_id: Optional[int] = Field(default=None, foreign_key="maintenancerecord.id")

    name: str                               # display name, e.g. "Lease Agreement 2025"
    document_type: Optional[str] = None     # lease, warranty, inspection, insurance, other
    file_path: Optional[str] = None         # future: path or S3 key
    uploaded_at: date = Field(default_factory=date.today)
    notes: Optional[str] = None


class Loan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    property_id: int = Field(foreign_key="property.id")

    # Labels
    label: Optional[str] = None     # e.g. "Primary Mortgage", "HELOC"
    lender: Optional[str] = None    # e.g. "Wells Fargo"

    # Origination terms
    original_balance: Decimal = Field(max_digits=12, decimal_places=2)
    interest_rate: Decimal = Field(max_digits=12, decimal_places=3)     # annual %
    loan_term_years: int = Field(default=30)
    origination_date: date     # closing / first payment date

    # Manual override (used instead of formula if set)
    balance_override: Optional[Decimal] = Field(default=None, max_digits=12, decimal_places=2)
    balance_override_date: Optional[date] = None # when override was recorded

    is_active: bool = Field(default=True) # flag paid-off loans without deleting them
