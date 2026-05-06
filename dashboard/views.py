from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    from itr.models import ITRFiling
    from ai_ca.models import ChatSession
    from financial.models import FinancialProfile

    itr = ITRFiling.objects.filter(user=request.user, tax_year='2024-25').first()
    recent_chats = ChatSession.objects.filter(user=request.user).order_by('-created_at')[:3]
    try:
        fin_profile = FinancialProfile.objects.get(user=request.user)
    except FinancialProfile.DoesNotExist:
        fin_profile = None

    return render(request, 'dashboard/home.html', {
        'itr': itr,
        'recent_chats': recent_chats,
        'fin_profile': fin_profile,
    })

def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    return render(request, 'landing.html')
