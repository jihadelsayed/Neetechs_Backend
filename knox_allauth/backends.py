
from typing import Optional
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


class EmailOrPhoneBackend(ModelBackend):
    """
    Authenticate with either email or phone in the `username` field.
    """

    def authenticate(
        self,
        request,
        username: Optional[str] = None,
        password: Optional[str] = None,
        **kwargs,
    ):
        if username is None or password is None:
            # Support DRF / custom clients passing `email` or `phone` explicitly
            username = kwargs.get("email") or kwargs.get("phone")
            if username is None:
                return None

        UserModel = get_user_model()
        ident = str(username).strip()

        # Try email (case-insensitive) or phone (exact)
        qs = UserModel.objects.all()
        user = (
            qs.filter(Q(email__iexact=ident) | Q(phone=ident))
            .order_by("-is_active")
            .first()
        )
        if not user:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
