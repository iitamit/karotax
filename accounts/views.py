from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
import json
from .forms import RegisterForm, LoginForm, ProfileSetupForm
from .models import User

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to KaroTax, {user.first_name}! Let\'s set up your profile.')
            return redirect('accounts:setup_profile')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'dashboard:home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {
        'form': form,
        'google_client_id': settings.GOOGLE_CLIENT_ID,
    })


@require_POST
def google_id_login_view(request):
    try:
        payload = json.loads(request.body)
        credential = payload.get('credential', '')
        token_info = id_token.verify_oauth2_token(
            credential,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID,
        )
    except (ValueError, json.JSONDecodeError):
        return JsonResponse({'error': 'Invalid Google login response.'}, status=400)

    email = token_info.get('email', '').lower()
    if not email or not token_info.get('email_verified'):
        return JsonResponse({'error': 'Google email is not verified.'}, status=400)

    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'username': email,
            'first_name': token_info.get('given_name', ''),
            'last_name': token_info.get('family_name', ''),
        },
    )

    changed = False
    if created:
        user.set_unusable_password()
        changed = True
    if not user.username:
        user.username = email
        changed = True
    if not user.first_name and token_info.get('given_name'):
        user.first_name = token_info['given_name']
        changed = True
    if not user.last_name and token_info.get('family_name'):
        user.last_name = token_info['family_name']
        changed = True
    if changed:
        user.save()

    login(request, user)
    return JsonResponse({'redirect_url': settings.LOGIN_REDIRECT_URL})

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def setup_profile(request):
    if request.method == 'POST':
        form = ProfileSetupForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_profile_complete = True
            user.save()
            messages.success(request, 'Profile saved! You are all set.')
            return redirect('dashboard:home')
    else:
        form = ProfileSetupForm(instance=request.user)
    return render(request, 'accounts/setup_profile.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')
