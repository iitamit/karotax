from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FinancialProfile, InvestmentRecommendation
from .planner import generate_plan

@login_required
def financial_home(request):
    try:
        profile = FinancialProfile.objects.get(user=request.user)
        recommendations = profile.recommendations.all().order_by('-created_at')[:10]
    except FinancialProfile.DoesNotExist:
        profile = None
        recommendations = []
    return render(request, 'financial/home.html', {
        'profile': profile,
        'recommendations': recommendations,
    })

@login_required
def setup_profile(request):
    profile, _ = FinancialProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile.monthly_income = float(request.POST.get('monthly_income', 0).replace(',','') or 0)
        profile.monthly_expenses = float(request.POST.get('monthly_expenses', 0).replace(',','') or 0)
        profile.existing_savings = float(request.POST.get('existing_savings', 0).replace(',','') or 0)
        profile.risk_profile = request.POST.get('risk_profile', 'moderate')
        profile.primary_goal = request.POST.get('primary_goal', 'wealth_creation')
        profile.goal_timeline_years = int(request.POST.get('goal_timeline_years', 5))
        profile.save()

        # Generate plan
        InvestmentRecommendation.objects.filter(profile=profile).delete()
        recs = generate_plan(profile)
        for r in recs:
            InvestmentRecommendation.objects.create(profile=profile, **r)

        messages.success(request, 'Your financial plan is ready!')
        return redirect('financial:home')

    return render(request, 'financial/setup.html', {'profile': profile})
