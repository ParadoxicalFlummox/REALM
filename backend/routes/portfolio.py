from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from database import get_session
from models import Property, Loan
from services.loan_logic import LoanService

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


@router.get("/summary")
def get_portfolio_summary(session: Session = Depends(get_session)):
    properties = session.exec(select(Property)).all()

    # Fetch all active loans in one query, then group by property_id
    all_loans = session.exec(select(Loan).where(Loan.is_active == True)).all()
    loans_by_property: dict[int, list] = {}
    for loan in all_loans:
        loans_by_property.setdefault(loan.property_id, []).append(loan)

    total_estimated_value = Decimal("0")
    total_loan_balance = Decimal("0")
    missing_value_count = 0

    property_rows = []
    for prop in properties:
        prop_loans = loans_by_property.get(prop.id, [])
        prop_loan_balance = sum(
            LoanService.calculate_balance(l) for l in prop_loans
        ) if prop_loans else Decimal("0")

        estimated_value = prop.estimated_value or Decimal("0")
        equity = estimated_value - prop_loan_balance
        ltv = (
            float((prop_loan_balance / estimated_value * 100).quantize(Decimal("0.01")))
            if estimated_value > 0
            else None
        )

        if prop.estimated_value:
            total_estimated_value += estimated_value
        else:
            missing_value_count += 1

        total_loan_balance += prop_loan_balance

        property_rows.append({
            "id": prop.id,
            "nickname": prop.nickname,
            "address": prop.address,
            "is_active": prop.is_active,
            "estimated_value": estimated_value if prop.estimated_value else None,
            "total_loan_balance": prop_loan_balance,
            "equity": equity if prop.estimated_value else None,
            "ltv": ltv,
            "loan_count": len(prop_loans),
        })

    total_equity = total_estimated_value - total_loan_balance
    portfolio_ltv = (
        float((total_loan_balance / total_estimated_value * 100).quantize(Decimal("0.01")))
        if total_estimated_value > 0
        else None
    )

    return {
        "property_count": len(properties),
        "missing_value_count": missing_value_count,
        "total_estimated_value": total_estimated_value,
        "total_loan_balance": total_loan_balance,
        "total_equity": total_equity,
        "portfolio_ltv": portfolio_ltv,
        "properties": property_rows,
    }
