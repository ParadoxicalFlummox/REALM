#from fastapi import APIRouter, Depends, HTTPException
from decimal import Decimal
from typing import List, Dict
from models import Transaction, TransactionType

class DashboardService:
    @staticmethod
    def get_expense_distribution(transactions: List[Transaction]) -> Dict[str, Decimal]:
        # Groups all expenses by category for leak detection charts
        dist = {}
        for t in transactions:
            if t.transaction_type == TransactionType.EXPENSE:
                dist[t.category] = dist.get(t.category, Decimal("0.00")) + t.amount
        return dist
    
    @staticmethod
    def calculate_rent_target(total_expenses: Decimal, desired_profit: Decimal, num_tennants: int) -> Decimal:
        if num_tennants <= 0:
            return Decimal("0.00")
        return (total_expenses + desired_profit) / num_tennants

    @staticmethod
    def get_financial_metrics(income: Decimal, expenses: Decimal, investment: Decimal):
        # Calculates the core financial metrics
        # Income/expenses should be ideally annualized for these to be standard.

        net_cash_flow = income - expenses

        # Operating expense ratio
        operating_expense_ratio = float((expenses / income) * 100) if income > 0 else 0.0

        # Cash on cash return or ROI
        return_on_income = float((net_cash_flow / investment) * 100) if investment > 0 else 0.0

        return {
            "net_cash_flow": net_cash_flow
            "operating_expense_ratio_percentage": round(operating_expense_ratio, 2)
            "return_on_income_percentage": round(return_on_income, 2)
        }