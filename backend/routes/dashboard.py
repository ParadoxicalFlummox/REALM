from datetime import date, timedelta
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from database import get_session
from models import Property, Transaction, TransactionType
from services.dashboard_logic import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

def validate_date_range(start: Optional[date], end: Optional[date]):
    if start and end and start > end: # Checks if a start date and end date are provided before checking if the start is after the end date
        raise HTTPException(
            status_code=400,
            detail="Error: Start date cannot be after end date. Time travel is not yet supported."
        )

@router.get("/insights/{property_id}")
def get_property_insights(
    property_id: int,
    start_date: Optional[date],
    end_date: Optional[date],
    target_profit: Decimal = Decimal("200.00"),
    num_tenants: int = Query(1, gt=0), 
    session: Session = Depends(get_session)
):
    validate_date_range(start_date, end_date)
    
    # Fetch the information about the current property
    prop = session.get(Property, property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    # Date handling (defaults to 6 months)
    end_date_time = end_date or date.today()
    start_date_time = start_date or (end_date_time - timedelta(days=180))

    # Filter at source query to save on resources
    statement = select(Transaction).where(
        Transaction.property_id == property_id,
        Transaction.transaction_date >= start_date_time,
        Transaction.transaction_date <= end_date_time
    )
    transactions = session.exec(statement).all()

    # Aggregration of data
    total_income = sum((t.amount for t in transactions if t.transaction_type == TransactionType.INCOME), Decimal("0.00"))
    total_expense = sum((t.amount for t in transactions if t.transaction_type == TransactionType.EXPENSE), Decimal("0.00"))

    metrics = DashboardService.get_financial_metrics(
        total_income,
        total_expense,
        prop.purchase_price
    )

    return{
        "property_nickname": prop.nickname,
        "period": {"start": start_date_time, "end": end_date_time},
        "metrics": metrics,
        "expense_distribution": DashboardService.get_expense_distribution(transactions),
        "rent_suggestions": {
            "break_even_per_tenant": DashboardService.calculate_rent_target(total_expense, Decimal("0"), num_tenants),
            "custom_profit_target_per_tenant": DashboardService.calculate_rent_target(total_expense, target_profit, num_tenants),
        }
    }