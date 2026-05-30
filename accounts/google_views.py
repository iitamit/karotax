from django.conf import settings

from allauth.socialaccount.providers.google.provider import GoogleProvider
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.views import OAuth2CallbackView, OAuth2LoginView


class LocalGoogleOAuth2Adapter(GoogleOAuth2Adapter):
    def get_callback_url(self, request, app):
        return settings.GOOGLE_OAUTH_CALLBACK_URL


GoogleProvider.oauth2_adapter_class = LocalGoogleOAuth2Adapter

oauth2_login = OAuth2LoginView.adapter_view(LocalGoogleOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(LocalGoogleOAuth2Adapter)
