from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Loan


class LoanService:

    @staticmethod
    def calculate_balance(loan: "Loan", as_of: date = None) -> Decimal:
        """
        Return the current outstanding balance for a loan.
        Uses balance_override if set, otherwise computes from amortization schedule.

        Formula: B = P * ((1+r)^n - (1+r)^k) / ((1+r)^n - 1)
          P = original_balance
          r = monthly interest rate
          n = total payment count (loan_term_years * 12)
          k = payments made (months elapsed since origination, capped at n)
        """
        if loan.balance_override is not None:
            return loan.balance_override

        if as_of is None:
            as_of = date.today()

        # Months elapsed since origination (year/month only — payments are monthly)
        k = (as_of.year - loan.origination_date.year) * 12 + \
            (as_of.month - loan.origination_date.month)
        n = loan.loan_term_years * 12
        k = max(0, min(k, n))

        if k >= n:
            return Decimal("0")  # fully paid off

        P = loan.original_balance
        r = (loan.interest_rate / Decimal("100")) / Decimal("12")

        if r == Decimal("0"):
            balance = P * Decimal(n - k) / Decimal(n)
        else:
            factor_n = (1 + r) ** n
            factor_k = (1 + r) ** k
            balance = P * (factor_n - factor_k) / (factor_n - 1)

        return balance.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
