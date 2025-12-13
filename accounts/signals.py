from django.dispatch import receiver

from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_added


def _extract_name(extra: dict) -> str | None:
    if not isinstance(extra, dict):
        return None

    full = extra.get("name")
    if full:
        return str(full).strip() or None

    given = extra.get("given_name") or extra.get("first_name")
    family = extra.get("family_name") or extra.get("last_name")
    if given or family:
        combined = " ".join([p for p in [given, family] if p]).strip()
        return combined or None

    display = extra.get("displayName") or extra.get("localizedFirstName")
    if display:
        return str(display).strip() or None

    return None


def _populate_user_name_from_social(user, account=None):
    if not account:
        return

    extra = getattr(account, "extra_data", None) or {}
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
    # If signup happened via social login, allauth provides sociallogin in kwargs
    sociallogin = kwargs.get("sociallogin")
    if sociallogin and getattr(sociallogin, "account", None):
        _populate_user_name_from_social(user, sociallogin.account)


@receiver(social_account_added)
def handle_social_account_added(request, sociallogin, **kwargs):
    _populate_user_name_from_social(sociallogin.user, sociallogin.account)
