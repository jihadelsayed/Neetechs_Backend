
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
from webauthn.helpers.structs import (
    UserVerificationRequirement,
    PublicKeyCredentialDescriptor,
)

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
    challenge = cache.get(f"register_challenge:{user_id}")

    result = verify_registration_response(
        expected_rp_id=RP_ID,
        expected_origin=f"https://{RP_ID}",
        credential=data,
        expected_challenge=challenge,
        user_verification_required=True,
    )

    # TODO: Persist result.credential_id (bytes), result.public_key (COSE key bytes), result.sign_count (int)
    # Example:
    # save_webauthn_credential(
    #     user_id=user_id,
    #     credential_id=result.credential_id,
    #     public_key=result.credential_public_key,
    #     sign_count=result.sign_count,
    # )
    return JsonResponse({"status": "ok"})


@csrf_exempt
def begin_authentication(request):
    data = json.loads(request.body)
    user_id = str(data["userId"])

    # TODO: Load credential_id bytes list from DB for this user
    # Example: stored_ids = [cred.credential_id for cred in get_user_credentials(user_id)]
    stored_ids = [
        # base64.urlsafe_b64decode("...")  # bytes of credential_id
    ]

    allow_credentials = [
        PublicKeyCredentialDescriptor(id=cid, type="public-key") for cid in stored_ids
    ] if stored_ids else None

    options = generate_authentication_options(
        rp_id=RP_ID,
        allow_credentials=allow_credentials,
        user_verification=UserVerificationRequirement.PREFERRED,
    )

    cache.set(f"auth_challenge:{user_id}", options.challenge, timeout=300)
    return JsonResponse(options.model_dump())


@csrf_exempt
def complete_authentication(request):
    data = json.loads(request.body)
    user_id = str(data["userId"])
    challenge = cache.get(f"auth_challenge:{user_id}")

    # TODO: Load the matching credential from DB using the credential ID in `data`
    # Example:
    # cred = get_credential_by_id(base64url_to_bytes(data["rawId"]))
    # public_key = cred.public_key
    # sign_count = cred.sign_count
    credential_public_key = None  # bytes
    sign_count = 0  # int

    result = verify_authentication_response(
        expected_rp_id=RP_ID,
        expected_origin=f"https://{RP_ID}",
        credential=data,
        expected_challenge=challenge,
        credential_public_key=credential_public_key,
        sign_count=sign_count,
        user_verification_required=True,
    )

    # TODO: Update stored sign_count to result.new_sign_count
    # update_credential_sign_count(cred_id=..., new_sign_count=result.new_sign_count)

    return JsonResponse({"status": "ok", "sign_count": result.new_sign_count})
