from django.urls import path
from . import views

app_name = 'itr'
urlpatterns = [
    path('', views.itr_home, name='home'),
    path('start/', views.start_filing, name='start'),
    path('step/<int:step>/', views.filing_step, name='step'),
    path('success/', views.itr_success, name='success'),
]
