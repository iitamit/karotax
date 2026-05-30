from django.conf import settings
from django.shortcuts import redirect


class LocalhostCanonicalMiddleware:
    """Use one localhost hostname so Google OAuth redirect URIs stay stable."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DEBUG and request.get_host() == "127.0.0.1:8000":
            return redirect(f"http://localhost:8000{request.get_full_path()}", permanent=False)

        return self.get_response(request)
