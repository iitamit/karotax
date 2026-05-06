"""
Indian Income Tax Calculator - FY 2024-25
Supports Old and New Tax Regime
"""

def calculate_tax(gross_income: float, deductions: float, regime: str) -> float:
    if regime == 'old':
        taxable = max(0, gross_income - deductions)
        return _old_regime_tax(taxable)
    else:
        taxable = max(0, gross_income - 75000)  # Standard deduction in new regime
        return _new_regime_tax(taxable)


def _old_regime_tax(taxable_income: float) -> float:
    tax = 0.0
    slabs = [
        (250000, 0.00),
        (500000, 0.05),
        (1000000, 0.20),
        (float('inf'), 0.30),
    ]
    prev = 0
    for limit, rate in slabs:
        if taxable_income <= prev:
            break
        taxable_in_slab = min(taxable_income, limit) - prev
        tax += taxable_in_slab * rate
        prev = limit

    # Rebate u/s 87A (income <= 5L, tax = 0)
    if taxable_income <= 500000:
        tax = 0

    # 4% Health & Education Cess
    tax += tax * 0.04
    return round(tax, 2)


def _new_regime_tax(taxable_income: float) -> float:
    tax = 0.0
    slabs = [
        (300000, 0.00),
        (600000, 0.05),
        (900000, 0.10),
        (1200000, 0.15),
        (1500000, 0.20),
        (float('inf'), 0.30),
    ]
    prev = 0
    for limit, rate in slabs:
        if taxable_income <= prev:
            break
        taxable_in_slab = min(taxable_income, limit) - prev
        tax += taxable_in_slab * rate
        prev = limit

    # Rebate u/s 87A (income <= 7L, tax = 0)
    if taxable_income <= 700000:
        tax = 0

    # 4% Health & Education Cess
    tax += tax * 0.04
    return round(tax, 2)


def get_ai_regime_suggestion(income: float, deductions: float, old_tax: float, new_tax: float) -> str:
    savings = abs(old_tax - new_tax)
    better = 'Old Regime' if old_tax < new_tax else 'New Regime'
    worse = 'New Regime' if old_tax < new_tax else 'Old Regime'

    if savings < 5000:
        return (f"Both regimes give almost the same result for you. "
                f"Difference is just ₹{savings:,.0f}. "
                f"We suggest {better} since your deductions of ₹{deductions:,.0f} "
                f"are {'benefiting' if old_tax < new_tax else 'not helping'} you.")

    return (f"✅ {better} saves you ₹{savings:,.0f} more tax! "
            f"Your tax under {better}: ₹{min(old_tax,new_tax):,.0f} vs "
            f"{worse}: ₹{max(old_tax,new_tax):,.0f}. "
            f"{'Your deductions of ₹' + f'{deductions:,.0f} are working well for you.' if old_tax < new_tax else 'Your deductions are low, so new regime is better.'}")


def format_inr(amount: float) -> str:
    """Format number as Indian Rupees with commas"""
    if amount >= 10000000:  # 1 crore
        return f"₹{amount/10000000:.2f} Cr"
    elif amount >= 100000:  # 1 lakh
        return f"₹{amount/100000:.2f} L"
    else:
        return f"₹{amount:,.0f}"
