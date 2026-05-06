from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import ChatSession, ChatMessage
from .gemini_service import get_ai_response
import json
from django.views.decorators.csrf import ensure_csrf_cookie

QUICK_QUESTIONS = [
    ("💰 80C Deductions", "What are the best 80C deductions I can use to save tax?"),
    ("📊 Old vs New Regime", "Which tax regime is better for me — old or new?"),
    ("📅 ITR Deadline", "What is the last date to file ITR for FY 2024-25?"),
    ("🏠 HRA Exemption", "How do I calculate my HRA exemption?"),
    ("📈 Best Investment", "Where should I invest my savings for tax saving and growth?"),
    ("🧾 GST Registration", "When do I need to register for GST?"),
    ("💼 Freelancer Tax", "How is tax calculated for a freelancer in India?"),
    ("🏦 NPS Benefits", "What are the tax benefits of investing in NPS?"),
]

@login_required
def chat_home(request):
    sessions = ChatSession.objects.filter(user=request.user).order_by('-created_at')[:10]
    return render(request, 'ai_ca/chat_home.html', {
        'sessions': sessions,
        'quick_questions': QUICK_QUESTIONS,
    })

@login_required
def new_session(request):
    topic = request.GET.get('topic', 'general')
    session = ChatSession.objects.create(user=request.user, topic=topic)
    return redirect('ai_ca:chat', session_id=session.id)

@login_required
def chat_view(request, session_id):
    session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    messages = session.messages.all()
    sessions = ChatSession.objects.filter(user=request.user).order_by('-created_at')[:10]
    return render(request, 'ai_ca/chat.html', {
        'session': session,
        'messages': messages,
        'sessions': sessions,
        'quick_questions': QUICK_QUESTIONS,
    })

@login_required
@require_POST
def send_message(request, session_id):
    session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    data = json.loads(request.body)
    user_message = data.get('message', '').strip()

    if not user_message:
        return JsonResponse({'error': 'Empty message'}, status=400)

    # Save user message
    ChatMessage.objects.create(session=session, role='user', content=user_message)

    # Update session title from first message
    if session.messages.count() == 1:
        session.title = user_message[:80]
        session.save()

# FIXED CODE
    all_messages = list(session.messages.all())
    # Exclude the last message (the one we just saved) to avoid sending it twice
    history = [{'role': m.role, 'content': m.content} for m in all_messages[:-1]]

    # Get user context
    user_context = {
        'income_type': request.user.income_type,
        'city': request.user.city,
    }

    # Get AI response
    ai_reply = get_ai_response(user_message, history, user_context)

    # Save AI response
    ChatMessage.objects.create(session=session, role='assistant', content=ai_reply)

    return JsonResponse({'reply': ai_reply, 'session_title': session.title})

@login_required
def delete_session(request, session_id):
    session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    session.delete()
    return redirect('ai_ca:home')

@ensure_csrf_cookie
def public_chat(request):
    """Public AI CA chat — no login required. Uses session for history."""
    # Fallback quick questions if you don't have them imported
    quick_questions = getattr(request, 'QUICK_QUESTIONS', [
        ("ITR kab file karna hai?", "ITR filing last date kya hai?"),
        ("New vs Old Regime?", "Mere liye New tax regime better hai ya Old?"),
        ("20 Lakh Invest karna hai", "I have 20 lakhs, where to invest?"),
        ("GST Registration Limit", "GST registration ki limit kya hai?")
    ])
    
    return render(request, 'ai_ca/public_chat.html', {
        'quick_questions': quick_questions,
    })

@require_POST
def public_send_message(request):
    """Handle messages from public (non-logged-in) users via session storage."""
    data = json.loads(request.body)
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return JsonResponse({'error': 'Empty message'}, status=400)
    
    # Get history from session (max 10 messages for context)
    history = request.session.get('public_chat_history', [])
    
    # Get AI response
    ai_reply = get_ai_response(user_message, history, user_context=None)
    
    # Save to session (keep last 20 messages = 10 exchanges)
    history.append({'role': 'user', 'content': user_message})
    history.append({'role': 'assistant', 'content': ai_reply})
    if len(history) > 20:
        history = history[-20:]
    request.session['public_chat_history'] = history
    request.session.modified = True
    
    return JsonResponse({'reply': ai_reply})