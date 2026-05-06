from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import ITRFiling, IncomeDetails, DeductionDetails
from .tax_calculator import calculate_tax, get_ai_regime_suggestion
import json

@login_required
def itr_home(request):
    filing = ITRFiling.objects.filter(user=request.user, tax_year='2024-25').first()
    return render(request, 'itr/home.html', {'filing': filing})

@login_required
def start_filing(request):
    filing, created = ITRFiling.objects.get_or_create(
        user=request.user, tax_year='2024-25',
        defaults={'status': 'draft', 'current_step': 1}
    )
    return redirect('itr:step', step=filing.current_step)

@login_required
def filing_step(request, step):
    filing = get_object_or_404(ITRFiling, user=request.user, tax_year='2024-25')
    steps = {
        1: ('itr/steps/step1_income_type.html', 'Income Type'),
        2: ('itr/steps/step2_income.html', 'Income Details'),
        3: ('itr/steps/step3_deductions.html', 'Deductions & 80C'),
        4: ('itr/steps/step4_review.html', 'Tax Summary'),
        5: ('itr/steps/step5_submit.html', 'Submit ITR'),
    }
    template, title = steps.get(step, steps[1])

    income = IncomeDetails.objects.filter(filing=filing).first()
    deductions = DeductionDetails.objects.filter(filing=filing).first()

    if request.method == 'POST':
        if step == 1:
            filing.itr_type = request.POST.get('itr_type', 'ITR-1')
            filing.current_step = 2
            filing.save()
            return redirect('itr:step', step=2)

        elif step == 2:
            income, _ = IncomeDetails.objects.get_or_create(filing=filing)
            fields = ['basic_salary', 'hra_received', 'hra_exemption', 'other_allowances',
                      'freelance_income', 'business_income', 'interest_income', 'rental_income',
                      'capital_gains_stcg', 'capital_gains_ltcg', 'other_income',
                      'tds_deducted', 'advance_tax_paid']
            for f in fields:
                val = request.POST.get(f, '0').replace(',', '') or '0'
                setattr(income, f, float(val))
            income.save()
            filing.total_income = income.total()
            filing.current_step = 3
            filing.save()
            return redirect('itr:step', step=3)

        elif step == 3:
            deductions, _ = DeductionDetails.objects.get_or_create(filing=filing)
            fields = ['ppf', 'elss', 'epf', 'lic_premium', 'home_loan_principal',
                      'tuition_fees', 'nsc', 'health_insurance_self', 'health_insurance_parents',
                      'nps_80ccd', 'home_loan_interest_24b', 'education_loan_80e',
                      'donation_80g', 'savings_interest_80tta']
            for f in fields:
                val = request.POST.get(f, '0').replace(',', '') or '0'
                setattr(deductions, f, float(val))
            deductions.save()

            # Calculate tax for both regimes and recommend
            income_val = float(filing.total_income)
            ded_val = float(deductions.total())
            old_tax = calculate_tax(income_val, ded_val, 'old')
            new_tax = calculate_tax(income_val, 0, 'new')
            suggestion = get_ai_regime_suggestion(income_val, ded_val, old_tax, new_tax)

            filing.total_deductions = ded_val
            filing.taxable_income = max(0, income_val - ded_val)
            filing.tax_liability = min(old_tax, new_tax)
            filing.ai_regime_suggestion = suggestion
            filing.regime = 'old' if old_tax <= new_tax else 'new'
            filing.current_step = 4
            filing.save()
            return redirect('itr:step', step=4)

        elif step == 4:
            filing.regime = request.POST.get('regime', filing.regime)
            income_val = float(filing.total_income)
            ded_val = float(filing.total_deductions) if filing.regime == 'old' else 0
            filing.tax_liability = calculate_tax(income_val, ded_val, filing.regime)
            tds = float(income.tds_deducted) + float(income.advance_tax_paid) if income else 0
            filing.tax_paid = tds
            filing.refund_or_payable = tds - float(filing.tax_liability)
            filing.current_step = 5
            filing.save()
            return redirect('itr:step', step=5)

        elif step == 5:
            filing.status = 'submitted'
            filing.save()
            return redirect('itr:success')

    context = {
        'filing': filing,
        'income': income,
        'deductions': deductions,
        'step': step,
        'step_title': title,
        'total_steps': 5,
    }
    if step == 4 and income and deductions:
        income_val = float(filing.total_income)
        context['old_tax'] = calculate_tax(income_val, float(deductions.total()), 'old')
        context['new_tax'] = calculate_tax(income_val, 0, 'new')

    return render(request, template, context)

@login_required
def itr_success(request):
    filing = get_object_or_404(ITRFiling, user=request.user, tax_year='2024-25')
    return render(request, 'itr/success.html', {'filing': filing})

@login_required
def itr_urls_file(request):
    pass
