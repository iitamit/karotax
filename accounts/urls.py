from django.urls import path
from . import views
from . import google_views

app_name = 'accounts'
urlpatterns = [
    path('google/login/', google_views.oauth2_login, name='google_login'),
    path('google/login/callback', google_views.oauth2_callback, name='google_callback'),
    path('google/login/callback/', google_views.oauth2_callback, name='google_callback_slash'),
    path('google/id-login/', views.google_id_login_view, name='google_id_login'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('setup-profile/', views.setup_profile, name='setup_profile'),
    path('profile/', views.profile_view, name='profile'),
]
