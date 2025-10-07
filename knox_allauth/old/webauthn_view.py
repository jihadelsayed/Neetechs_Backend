import json
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache

from webauthn import (
    generate_registration_options,
    generate_authentication_options,
    verify_registration_response,
    verify_authentication_response,
)
from webauthn.helpers.structs import UserVerificationRequirement

RP_ID = "neetechs.com"
RP_NAME = "Neetechs"

@csrf_exempt
def begin_registration(request):
    data = json.loads(request.body)
    user_id = str(data["userId"])
    username = data["username"]

    options = generate_registration_options(
        rp_id=RP_ID,
        rp_name=RP_NAME,
        user_id=user_id.encode(),
        user_name=username,
        user_display_name=username,
        user_verification=UserVerificationRequirement.PREFERRED,
    )

    cache.set(f"register_challenge:{user_id}", options.challenge, timeout=300)
    return JsonResponse(options.model_dump())


@csrf_exempt
def complete_registration(request):
    data = json.loads(request.body)
    user_id = str(data["userId"])
    challenge_b64 = cache.get(f"register_challenge:{user_id}")

    result = verify_registration_response(
        expected_rp_id=RP_ID,
        expected_origin=f"https://{RP_ID}",
        credential=data,
        expected_challenge=challenge_b64,
        user_verification_required=True,
    )

    # Save result.credential_id, result.public_key, result.sign_count, etc. to DB here
    return JsonResponse({"status": "ok"})


@csrf_exempt
def begin_authentication(request):
    data = json.loads(request.body)
    user_id = str(data["userId"])

    # TODO: Replace with real credential IDs from DB
    stored_credential_ids = [
        base64.b64decode("...")  # Replace with actual Base64URL-encoded credential ID bytes
    ]

    options = generate_authentication_options(
        rp_id=RP_ID,
        allow_credentials=stored_credential_ids,
        user_verification=UserVerificationRequirement.PREFERRED,
    )

    cache.set(f"auth_challenge:{user_id}", options.challenge, timeout=300)
    return JsonResponse(options.model_dump())


@csrf_exempt
def complete_authentication(request):
    data = json.loads(request.body)
    user_id = str(data["userId"])
    challenge = cache.get(f"auth_challenge:{user_id}")

    result = verify_authentication_response(
        expected_rp_id=RP_ID,
        expected_origin=f"https://{RP_ID}",
        credential=data,
        expected_challenge=challenge,
        credential_public_key=None,  # Replace with public key object from DB
        sign_count=0,                # Replace with stored sign count
        user_verification_required=True,
    )

    # Update stored sign_count with result.new_sign_count
    return JsonResponse({"status": "ok", "sign_count": result.new_sign_count})
