from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from database import get_session
from models import Deal
from services.deal_logic import DealService

router = APIRouter(prefix="/deals", tags=["Deals"])


# --- Input schema (shared by calculate and save) ---
# We use Deal directly as the body type for saving.
# For calculate we build a lightweight Pydantic model so we don't need an id/created_at.

from pydantic import BaseModel

class DealInput(BaseModel):
    name: Optional[str] = None
    address: str
    property_id: Optional[int] = None

    # Purchase
    purchase_price: Decimal
    down_payment: Decimal
    closing_costs: Decimal = Decimal("0")
    rehab_cost: Decimal = Decimal("0")

    # Loan
    interest_rate: Decimal
    loan_term_years: int = 30

    # Monthly income / expenses
    monthly_rent: Decimal
    vacancy_rate: Decimal = Decimal("5.0")
    monthly_property_tax: Decimal = Decimal("0")
    insurance: Decimal = Decimal("0")
    hoa: Decimal = Decimal("0")
    maintenance: Decimal = Decimal("0")
    capex: Decimal = Decimal("0")
    utilities: Decimal = Decimal("0")
    lawn_snow: Decimal = Decimal("0")


def _run_calc(data: DealInput) -> dict:
    return DealService.calculate(
        purchase_price=data.purchase_price,
        down_payment=data.down_payment,
        closing_costs=data.closing_costs,
        rehab_cost=data.rehab_cost,
        interest_rate=data.interest_rate,
        loan_term_years=data.loan_term_years,
        monthly_rent=data.monthly_rent,
        vacancy_rate=data.vacancy_rate,
        monthly_property_tax=data.monthly_property_tax,
        insurance=data.insurance,
        hoa=data.hoa,
        maintenance=data.maintenance,
        capex=data.capex,
        utilities=data.utilities,
        lawn_snow=data.lawn_snow,
    )


@router.post("/calculate")
def calculate_deal(data: DealInput):
    """Run the deal math and return results — no database write."""
    return _run_calc(data)


@router.post("/")
def save_deal(data: DealInput, session: Session = Depends(get_session)):
    """Calculate and save a deal snapshot to the database."""
    results = _run_calc(data)

    deal = Deal(
        name=data.name,
        address=data.address,
        property_id=data.property_id,
        purchase_price=data.purchase_price,
        down_payment=data.down_payment,
        closing_costs=data.closing_costs,
        rehab_cost=data.rehab_cost,
        interest_rate=data.interest_rate,
        loan_term_years=data.loan_term_years,
        monthly_rent=data.monthly_rent,
        vacancy_rate=data.vacancy_rate,
        monthly_property_tax=data.monthly_property_tax,
        insurance=data.insurance,
        hoa=data.hoa,
        maintenance=data.maintenance,
        capex=data.capex,
        utilities=data.utilities,
        lawn_snow=data.lawn_snow,
        **results,
    )

    session.add(deal)
    session.commit()
    session.refresh(deal)
    return deal


@router.get("/")
def list_deals(
    property_id: Optional[int] = Query(default=None),
    session: Session = Depends(get_session),
):
    """List saved deals. Filter by property_id if provided."""
    statement = select(Deal)
    if property_id is not None:
        statement = statement.where(Deal.property_id == property_id)
    return session.exec(statement).all()


@router.get("/{deal_id}")
def get_deal(deal_id: int, session: Session = Depends(get_session)):
    deal = session.get(Deal, deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal


@router.delete("/{deal_id}")
def delete_deal(deal_id: int, session: Session = Depends(get_session)):
    deal = session.get(Deal, deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    session.delete(deal)
    session.commit()
    return {"message": f"Deal {deal_id} deleted successfully"}
