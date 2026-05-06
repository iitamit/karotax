from django.urls import path
from . import views

app_name = 'financial'
urlpatterns = [
    path('', views.financial_home, name='home'),
    path('setup/', views.setup_profile, name='setup'),
]
