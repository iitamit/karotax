from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views import landing

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name='landing'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('itr/', include('itr.urls')),
    path('ai-ca/', include('ai_ca.urls')),
    path('financial/', include('financial.urls')),
    path('dashboard/', include('dashboard.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
