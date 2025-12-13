from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter

class AccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        base = settings.FRONTEND_URL.rstrip("/")
        return f"{base}/confirm-email/{emailconfirmation.key}"
