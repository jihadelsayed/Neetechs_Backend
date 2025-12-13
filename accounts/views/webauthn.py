import json

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from webauthn import (
    generate_registration_options,
    generate_authentication_options,
    verify_registration_response,
    verify_authentication_response,
)
from webauthn.helpers.structs import (
    UserVerificationRequirement,
    PublicKeyCredentialDescriptor,
)

RP_ID = getattr(settings, "WEBAUTHN_RP_ID", "neetechs.com")
RP_NAME = getattr(settings, "WEBAUTHN_RP_NAME", "Neetechs")

CHALLENGE_TTL_SECONDS = 300


def _disabled():
    return JsonResponse({"detail": "WebAuthn is disabled."}, status=404)


def _safe_json(request):
    try:
        return json.loads(request.body or b"{}")
    except Exception:
        return None


def _client_key(request) -> str:
    """
    Tie challenge to a caller-specific key.
    Best: authenticated user id. Fallback: session key.
    """
    user = getattr(request, "user", None)
    if user and getattr(user, "is_authenticated", False):
        return f"user:{user.id}"

    # Session-based fallback (still better than trusting userId from client)
    sk = getattr(request, "session", None)
    if sk and getattr(sk, "session_key", None):
        return f"session:{sk.session_key}"

    # Absolute fallback (not great but prevents crashing)
    return "anon"


@csrf_exempt
@require_POST
def begin_registration(request):
    if not getattr(settings, "WEBAUTHN_ENABLED", False):
        return _disabled()

    data = _safe_json(request)
    if data is None:
        return JsonResponse({"detail": "Invalid JSON."}, status=400)

    # If authenticated, use server truth. Otherwise allow explicit fields (dev only).
    if getattr(request.user, "is_authenticated", False):
        user_id = str(request.user.id)
        username = request.user.username
    else:
        if not getattr(settings, "DEBUG", False):
            return JsonResponse({"detail": "Authentication required."}, status=401)
        user_id = str(data.get("userId") or "")
        username = str(data.get("username") or "")
        if not user_id or not username:
            return JsonResponse({"detail": "userId and username are required."}, status=400)

    options = generate_registration_options(
        rp_id=RP_ID,
        rp_name=RP_NAME,
        user_id=user_id.encode(),
        user_name=username,
        user_display_name=username,
        user_verification=UserVerificationRequirement.PREFERRED,
    )

    cache.set(f"webauthn:register_challenge:{_client_key(request)}", options.challenge, timeout=CHALLENGE_TTL_SECONDS)
    return JsonResponse(options.model_dump())


@csrf_exempt
@require_POST
def complete_registration(request):
    if not getattr(settings, "WEBAUTHN_ENABLED", False):
        return _disabled()

    data = _safe_json(request)
    if data is None:
        return JsonResponse({"detail": "Invalid JSON."}, status=400)

    challenge_key = f"webauthn:register_challenge:{_client_key(request)}"
    challenge = cache.get(challenge_key)
    if not challenge:
        return JsonResponse({"detail": "Registration challenge expired. Restart registration."}, status=400)

    try:
        result = verify_registration_response(
            expected_rp_id=RP_ID,
            expected_origin=f"https://{RP_ID}",
            credential=data,
            expected_challenge=challenge,
            user_verification_required=True,
        )
    except Exception:
        return JsonResponse({"detail": "Invalid registration response."}, status=400)
    finally:
        cache.delete(challenge_key)

    # TODO: persist:
    # result.credential_id (bytes)
    # result.credential_public_key (bytes)
    # result.sign_count (int)

    return JsonResponse({"status": "ok"})


@csrf_exempt
@require_POST
def begin_authentication(request):
    if not getattr(settings, "WEBAUTHN_ENABLED", False):
        return _disabled()

    # TODO: load stored credential IDs for authenticated user.
    # For now: allow_credentials=None means "discoverable credentials" if supported.
    stored_ids = []

    allow_credentials = (
        [PublicKeyCredentialDescriptor(id=cid, type="public-key") for cid in stored_ids]
        if stored_ids
        else None
    )

    options = generate_authentication_options(
        rp_id=RP_ID,
        allow_credentials=allow_credentials,
        user_verification=UserVerificationRequirement.PREFERRED,
    )

    cache.set(f"webauthn:auth_challenge:{_client_key(request)}", options.challenge, timeout=CHALLENGE_TTL_SECONDS)
    return JsonResponse(options.model_dump())


@csrf_exempt
@require_POST
def complete_authentication(request):
    if not getattr(settings, "WEBAUTHN_ENABLED", False):
        return _disabled()

    data = _safe_json(request)
    if data is None:
        return JsonResponse({"detail": "Invalid JSON."}, status=400)

    challenge_key = f"webauthn:auth_challenge:{_client_key(request)}"
    challenge = cache.get(challenge_key)
    if not challenge:
        return JsonResponse({"detail": "Authentication challenge expired. Restart login."}, status=400)

    # TODO: load matching credential from DB using credential ID in `data`
    credential_public_key = None  # bytes
    sign_count = 0  # int

    try:
        result = verify_authentication_response(
            expected_rp_id=RP_ID,
            expected_origin=f"https://{RP_ID}",
            credential=data,
            expected_challenge=challenge,
            credential_public_key=credential_public_key,
            sign_count=sign_count,
            user_verification_required=True,
        )
    except Exception:
        return JsonResponse({"detail": "Invalid authentication response."}, status=400)
    finally:
        cache.delete(challenge_key)

    # TODO: update stored sign_count to result.new_sign_count

    return JsonResponse({"status": "ok", "sign_count": result.new_sign_count})
