from decimal import Decimal, ROUND_HALF_UP


class DealService:

    @staticmethod
    def calculate(
        purchase_price: Decimal,
        down_payment: Decimal,
        closing_costs: Decimal,
        rehab_cost: Decimal,
        interest_rate: Decimal,
        loan_term_years: int,
        monthly_rent: Decimal,
        vacancy_rate: Decimal,
        monthly_property_tax: Decimal,
        insurance: Decimal,
        hoa: Decimal,
        maintenance: Decimal,
        capex: Decimal,
        utilities: Decimal,
        lawn_snow: Decimal,
    ) -> dict:
        # --- Loan ---
        loan_amount = purchase_price - down_payment

        r = (interest_rate / Decimal("100")) / Decimal("12")  # monthly interest rate
        n = loan_term_years * 12                               # total number of payments

        if r == 0:
            # 0% interest edge case (seller financing, etc.)
            monthly_mortgage = loan_amount / Decimal(n) if n > 0 else Decimal("0")
        else:
            factor = (1 + r) ** n
            monthly_mortgage = loan_amount * (r * factor) / (factor - 1)

        monthly_mortgage = monthly_mortgage.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # --- Income ---
        effective_rent = monthly_rent * (1 - vacancy_rate / Decimal("100"))

        # --- Operating expenses (excludes mortgage — standard NOI definition) ---
        operating_expenses = (
            monthly_property_tax + insurance + hoa +
            maintenance + capex + utilities + lawn_snow
        )

        # --- NOI ---
        monthly_noi = effective_rent - operating_expenses

        # --- Cash flow ---
        monthly_cash_flow = monthly_noi - monthly_mortgage
        annual_cash_flow = monthly_cash_flow * 12

        # --- Total cash invested ---
        total_cash_in = down_payment + closing_costs + rehab_cost

        # --- Cash-on-cash return ---
        cash_on_cash = (
            (annual_cash_flow / total_cash_in * 100)
            if total_cash_in > 0
            else Decimal("0")
        )

        # --- DSCR (Debt Service Coverage Ratio) ---
        # NOI / debt service. >1.0 means income covers mortgage. Lenders want >1.25.
        dscr = (
            monthly_noi / monthly_mortgage
            if monthly_mortgage > 0
            else Decimal("0")
        )

        # --- Break-even occupancy ---
        # Minimum occupancy % to cover all costs (mortgage + operating)
        total_monthly_costs = operating_expenses + monthly_mortgage
        break_even = (
            (total_monthly_costs / monthly_rent * 100)
            if monthly_rent > 0
            else Decimal("0")
        )

        # --- Tax figures ---
        annual_property_tax = monthly_property_tax * 12

        def q(val: Decimal, places: str = "0.01") -> Decimal:
            return val.quantize(Decimal(places), rounding=ROUND_HALF_UP)

        return {
            "monthly_mortgage": q(monthly_mortgage),
            "monthly_noi": q(monthly_noi),
            "monthly_cash_flow": q(monthly_cash_flow),
            "annual_cash_flow": q(annual_cash_flow),
            "annual_property_tax": q(annual_property_tax),
            "cash_on_cash_return": q(cash_on_cash, "0.0001"),
            "dscr": q(dscr, "0.0001"),
            "break_even_occupancy": q(break_even, "0.0001"),
            # Transparency fields — let the UI show the full derivation
            "effective_rent": q(effective_rent),
            "operating_expenses": q(operating_expenses),
            "total_monthly_payment": q(operating_expenses + monthly_mortgage),
        }
