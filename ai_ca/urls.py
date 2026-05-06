from django.urls import path
from . import views

app_name = 'ai_ca'
urlpatterns = [
    path('', views.chat_home, name='home'),
    path('new/', views.new_session, name='new_session'),
    path('chat/<int:session_id>/', views.chat_view, name='chat'),
    path('chat/<int:session_id>/send/', views.send_message, name='send_message'),
    path('chat/<int:session_id>/delete/', views.delete_session, name='delete_session'),
    path('public/', views.public_chat, name='public_chat'),
    path('public/send/', views.public_send_message, name='public_send'),
]
