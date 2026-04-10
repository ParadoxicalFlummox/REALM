from decimal import Decimal
from typing import Optional
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from pydantic import BaseModel

from database import get_session
from models import Loan, Property
from services.loan_logic import LoanService

router = APIRouter(tags=["Loans"])


# --- Input schema ---

class LoanCreate(BaseModel):
    property_id: int
    label: Optional[str] = None
    lender: Optional[str] = None
    original_balance: Decimal
    interest_rate: Decimal
    loan_term_years: int = 30
    origination_date: date
    balance_override: Optional[Decimal] = None
    balance_override_date: Optional[date] = None
    is_active: bool = True


class LoanUpdate(BaseModel):
    label: Optional[str] = None
    lender: Optional[str] = None
    original_balance: Optional[Decimal] = None
    interest_rate: Optional[Decimal] = None
    loan_term_years: Optional[int] = None
    origination_date: Optional[date] = None
    balance_override: Optional[Decimal] = None
    balance_override_date: Optional[date] = None
    is_active: Optional[bool] = None


# --- Helper ---

def _loan_with_balance(loan: Loan) -> dict:
    balance = LoanService.calculate_balance(loan)
    return {
        "id": loan.id,
        "property_id": loan.property_id,
        "label": loan.label,
        "lender": loan.lender,
        "original_balance": loan.original_balance,
        "current_balance": balance,
        "balance_is_override": loan.balance_override is not None,
        "balance_override": loan.balance_override,
        "balance_override_date": loan.balance_override_date,
        "interest_rate": loan.interest_rate,
        "loan_term_years": loan.loan_term_years,
        "origination_date": loan.origination_date,
        "is_active": loan.is_active,
    }


# --- Routes ---

@router.post("/loans/", tags=["Loans"])
def create_loan(data: LoanCreate, session: Session = Depends(get_session)):
    loan = Loan(**data.model_dump())
    session.add(loan)
    session.commit()
    session.refresh(loan)
    return _loan_with_balance(loan)


@router.get("/loans/", tags=["Loans"])
def list_loans(property_id: int = Query(...), session: Session = Depends(get_session)):
    loans = session.exec(select(Loan).where(Loan.property_id == property_id)).all()
    return [_loan_with_balance(l) for l in loans]


@router.patch("/loans/{loan_id}", tags=["Loans"])
def update_loan(loan_id: int, data: LoanUpdate, session: Session = Depends(get_session)):
    loan = session.get(Loan, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(loan, key, value)
    session.add(loan)
    session.commit()
    session.refresh(loan)
    return _loan_with_balance(loan)


@router.delete("/loans/{loan_id}", tags=["Loans"])
def delete_loan(loan_id: int, session: Session = Depends(get_session)):
    loan = session.get(Loan, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    session.delete(loan)
    session.commit()
    return {"message": f"Loan {loan_id} deleted"}


@router.get("/properties/{property_id}/equity", tags=["Loans"])
def get_equity(property_id: int, session: Session = Depends(get_session)):
    prop = session.get(Property, property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    loans = session.exec(
        select(Loan).where(Loan.property_id == property_id, Loan.is_active == True)
    ).all()

    loan_data = [_loan_with_balance(l) for l in loans]
    total_balance = sum(l["current_balance"] for l in loan_data)

    estimated_value = prop.estimated_value or Decimal("0")
    equity = estimated_value - total_balance
    ltv = (total_balance / estimated_value * 100) if estimated_value > 0 else Decimal("0")

    return {
        "estimated_value": estimated_value,
        "loans": loan_data,
        "total_loan_balance": total_balance,
        "equity": equity,
        "ltv": float(ltv.quantize(Decimal("0.01"))),
    }
