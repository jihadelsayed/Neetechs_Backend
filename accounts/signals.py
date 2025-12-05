
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_added
from allauth.socialaccount.models import SocialAccount


User = get_user_model()


def _extract_name(extra):
    # Try common provider keys
    full = extra.get("name")
    if full:
        return full

    given = extra.get("given_name") or extra.get("first_name")
    family = extra.get("family_name") or extra.get("last_name")
    if given or family:
        return " ".join([p for p in [given, family] if p]).strip()

    # Fallbacks some providers use
    display = extra.get("displayName") or extra.get("localizedFirstName")
    if display:
        return str(display)

    return None


def _populate_user_name_from_social(user, account: SocialAccount | None = None):
    if user.name and user.first_name:
        return

    acct = account or SocialAccount.objects.filter(user=user).first()
    if not acct:
        return

    extra = acct.extra_data or {}
    name = _extract_name(extra)
    if not name:
        return

    changed = False
    if not user.name:
        user.name = name
        changed = True
    if not user.first_name:
        user.first_name = name.split(" ")[0]
        changed = True
    if changed:
        user.save(update_fields=["name", "first_name"])


@receiver(user_signed_up)
def handle_user_signed_up(request, user, **kwargs):
    _populate_user_name_from_social(user)


@receiver(social_account_added)
def handle_social_account_added(request, sociallogin, **kwargs):
    _populate_user_name_from_social(sociallogin.user, sociallogin.account)
