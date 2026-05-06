"""Rule-based financial planner for Indian users"""

GOVT_SCHEMES = {
    'conservative': [
        {'title': 'Public Provident Fund (PPF)', 'category': 'Government Scheme',
         'description': 'Risk-free, tax-free returns at 7.1% p.a. Lock-in: 15 years. 80C benefit.', 
         'expected_return': '7.1% p.a.', 'risk_level': 'Very Low', 'tax_benefit': True},
        {'title': 'Sukanya Samriddhi Yojana (SSY)', 'category': 'Government Scheme',
         'description': 'For girl child education/marriage. 8.2% p.a., fully tax-free.',
         'expected_return': '8.2% p.a.', 'risk_level': 'Very Low', 'tax_benefit': True},
        {'title': 'Senior Citizen Savings Scheme', 'category': 'Government Scheme',
         'description': '8.2% p.a. quarterly payout. Max ₹30L. 80C benefit.',
         'expected_return': '8.2% p.a.', 'risk_level': 'Very Low', 'tax_benefit': True},
    ],
    'moderate': [
        {'title': 'ELSS Mutual Funds', 'category': 'Mutual Fund',
         'description': 'Tax-saving equity funds. 3-year lock-in. Historical returns 12-15% p.a.',
         'expected_return': '12-15% p.a.', 'risk_level': 'Medium', 'tax_benefit': True},
        {'title': 'National Pension System (NPS)', 'category': 'Pension',
         'description': 'Extra ₹50K deduction under 80CCD(1B). Market-linked retirement corpus.',
         'expected_return': '10-12% p.a.', 'risk_level': 'Medium', 'tax_benefit': True},
        {'title': 'Balanced/Hybrid Mutual Funds (SIP)', 'category': 'Mutual Fund',
         'description': '60% equity + 40% debt. Good for 3-5 year goals.',
         'expected_return': '10-12% p.a.', 'risk_level': 'Medium', 'tax_benefit': False},
    ],
    'aggressive': [
        {'title': 'Large Cap Index Funds (Nifty 50)', 'category': 'Mutual Fund',
         'description': 'Low-cost index investing. Best for long-term (7+ years). SIP recommended.',
         'expected_return': '12-14% p.a.', 'risk_level': 'Medium-High', 'tax_benefit': False},
        {'title': 'Mid & Small Cap Funds', 'category': 'Mutual Fund',
         'description': 'High growth potential. Volatile in short term. 7+ year horizon needed.',
         'expected_return': '14-18% p.a.', 'risk_level': 'High', 'tax_benefit': False},
        {'title': 'Direct Stocks (Blue Chip)', 'category': 'Equity',
         'description': 'Invest in Nifty 50 companies directly. Research required.',
         'expected_return': '12-20% p.a.', 'risk_level': 'High', 'tax_benefit': False},
    ]
}

def generate_plan(profile):
    surplus = profile.monthly_surplus()
    recommendations = []
    risk = profile.risk_profile

    # Emergency fund first (always)
    emergency_needed = float(profile.monthly_expenses) * 6
    recommendations.append({
        'title': '🆘 Emergency Fund (Priority 1)',
        'category': 'Safety Net',
        'description': (f"Keep 6 months of expenses (₹{emergency_needed:,.0f}) in a liquid fund or "
                       f"high-interest savings account. This is non-negotiable before any investment."),
        'suggested_amount': min(surplus * 0.3, emergency_needed / 12),
        'expected_return': '6-7% p.a.',
        'risk_level': 'Very Low',
        'tax_benefit': False,
    })

    # Get scheme recs based on risk
    schemes = GOVT_SCHEMES.get(risk, GOVT_SCHEMES['moderate'])
    for i, scheme in enumerate(schemes):
        allocation = surplus * [0.3, 0.25, 0.2][min(i, 2)]
        recommendations.append({**scheme, 'suggested_amount': max(500, allocation)})

    # Health Insurance (always recommend)
    recommendations.append({
        'title': '🏥 Health Insurance (Mediclaim)',
        'category': 'Insurance',
        'description': 'Min ₹5 lakh cover for yourself + family. 80D deduction up to ₹25K (₹50K if parents senior citizen).',
        'suggested_amount': 1500,
        'expected_return': 'N/A',
        'risk_level': 'N/A',
        'tax_benefit': True,
    })

    return recommendations
