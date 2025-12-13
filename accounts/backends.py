from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class EmailOrPhoneBackend(ModelBackend):
    """
    Authenticate with either email or phone provided in the `username` field
    (or `email` / `phone` kwargs for compatibility).
    """

    def authenticate(
        self,
        request,
        username: Optional[str] = None,
        password: Optional[str] = None,
        **kwargs,
    ):
        if password is None:
            return None

        ident = username or kwargs.get("email") or kwargs.get("phone")
        if not ident:
            return None

        ident = str(ident).strip()
        is_email = "@" in ident
        if is_email:
            ident = ident.lower()

        UserModel = get_user_model()

        # Email: case-insensitive
        # Phone: exact match (after stripping); leave formatting rules to input layer
        user = (
            UserModel.objects.filter(
                Q(email__iexact=ident) if is_email else Q(phone=ident)
            )
            .only("id", "password", "is_active")  # keep query light
            .first()
        )

        if not user:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
