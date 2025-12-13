from django.dispatch import receiver
from django.contrib.auth import get_user_model

from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_added
from allauth.socialaccount.models import SocialAccount

User = get_user_model()


def _extract_name(extra: dict) -> str | None:
    full = extra.get("name")
    if full:
        return str(full)

    given = extra.get("given_name") or extra.get("first_name")
    family = extra.get("family_name") or extra.get("last_name")
    if given or family:
        return " ".join([p for p in [given, family] if p]).strip()

    display = extra.get("displayName") or extra.get("localizedFirstName")
    if display:
        return str(display)

    return None


def _populate_user_name_from_social(user, account: SocialAccount | None = None):
    acct = account or SocialAccount.objects.filter(user=user).first()
    if not acct:
        return

    extra = acct.extra_data or {}
    full_name = _extract_name(extra)
    if not full_name:
        return

    parts = full_name.split()
    first = parts[0] if parts else ""
    last = " ".join(parts[1:]) if len(parts) > 1 else ""

    changed = []

    if not user.display_name:
        user.display_name = full_name
        changed.append("display_name")

    if not user.first_name and first:
        user.first_name = first
        changed.append("first_name")

    if not user.last_name and last:
        user.last_name = last
        changed.append("last_name")

    if changed:
        user.save(update_fields=changed)


@receiver(user_signed_up)
def handle_user_signed_up(request, user, **kwargs):
    _populate_user_name_from_social(user)


@receiver(social_account_added)
def handle_social_account_added(request, sociallogin, **kwargs):
    _populate_user_name_from_social(sociallogin.user, sociallogin.account)
