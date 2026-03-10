from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException
from services.dashboard_logic import DashboardService
from database import get_session
from typing import Optional

router = APIRouter(prefix="/dashboard")

@router.get("/insights/{property_id}")
def get_property_insights(
    property_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    target_profit: Decimal = Decimal("200.00"),
    num_tennants: int = 1,
    session: Session = Depends(get_session)
):
    
    # Fetch the information about the current property
    prop = session.get(Property, property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    # Date handling (defaults to 6 months)
    end_date = end_date or date.today()
    start_date = start_date or (end_date - timedelta(days=180))

    # Filter at source query to save on resources
    statement = select(transaction).where(
        Transaction.property_id == property_id,
        Transaction.transaction_date >= start_date,
        Transaction.transaction_date <= end_date
    )
    transactions = session.exec(statement).all()

    # Aggregration of data
    total_income = sum((t.amount for t in transactions if t.transaction_type == TransactionType.INCOME), Decimal("0.00"))
    total_expense = sum((t.amount for t in transactions if t.transaction_type == TransactionType.EXPENSE), Decimal("0.00"))

    # Call to the logic functions
    metrics = DashboardService.get_financial_metrics(
        total_income,
        total_expense,
        prop.investment_cost
    )

    expense_dist = DashboardService.get_expense_distribution(transactions)

    return{
        "property_name": prop.name,
        "period": {"start": start_date, "end": end_date},
        "metrics": metrics,
        "rent_suggestions": {
            "break_even_per_tennant": DashboardService.calculate_rent_target(total_expense, Decimal("0"), num_tennants),
            "custom_profit_target_per_tenant": DashboardService.calculate_rent_target(total_expense, target_profit, num_tennants),
            "metadata": {
                "applied_target_profit": target_profit,
                "applied_tennant_count": num_tennants
            }
        }
    }