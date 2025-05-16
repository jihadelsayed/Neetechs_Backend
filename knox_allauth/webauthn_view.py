import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from webauthn import get_webauthn_credentials

from webauthn import create_webauthn_credentials
from webauthn import verify_create_webauthn_credentials
from webauthn import metadata, types

@csrf_exempt
def begin_registration(request):
    data = json.loads(request.body)
    user_id = str(data["userId"])
    username = data["username"]

    rp = types.RelyingParty(id="neetechs.com", name="Neetechs")
    user = types.User(id=user_id.encode(), name=username, display_name=username)

    options, challenge = create_webauthn_credentials(
        rp=rp,
        user=user,
        user_verification=types.UserVerification.PREFERRED,
    )

    cache.set(f"register_challenge:{user_id}", challenge, timeout=300)
    return JsonResponse(options)




@csrf_exempt
def complete_registration(request):
    data = json.loads(request.body)
    user_id = str(data["userId"])
    challenge_b64 = cache.get(f"register_challenge:{user_id}")

    result = verify_create_webauthn_credentials(
        rp=types.RelyingParty(id="neetechs.com", name="Neetechs"),
        challenge_b64=challenge_b64,
        client_data_b64=data["clientData"],
        attestation_b64=data["attestationObject"],
        fido_metadata=metadata.FIDOMetadata(),
        user_verification_required=True
    )

    # save result.public_key, result.attestation, result.aaguid, result.sign_count
    return JsonResponse({"status": "ok"})


@csrf_exempt
def begin_authentication(request):
    data = json.loads(request.body)
    user_id = str(data["userId"])

    rp = types.RelyingParty(id="neetechs.com", name="Neetechs")

    # TODO: Replace with list of previously registered credential IDs from DB
    stored_credential_ids = [
        base64.b64decode("...")  # byte[] from DB
    ]

    options, challenge = get_webauthn_credentials(
        rp=rp,
        existing_keys=stored_credential_ids,
        user_verification=types.UserVerification.PREFERRED,
    )

    cache.set(f"auth_challenge:{user_id}", challenge, timeout=300)
    return JsonResponse(options)

from webauthn import verify_get_webauthn_credentials

@csrf_exempt
def complete_authentication(request):
    data = json.loads(request.body)
    user_id = str(data["userId"])
    challenge = cache.get(f"auth_challenge:{user_id}")

    # ⚠️ Extract the required fields from frontend
    client_data_b64 = data["clientData"]
    authenticator_data_b64 = data["authenticatorData"]
    signature_b64 = data["signature"]

    # ✅ Replace with stored user info from DB
    pubkey_alg = -7  # Example: -7 = ES256
    sign_count = 0
    public_key = None  # Should be the parsed key object, not a string

    rp = types.RelyingParty(id="neetechs.com", name="Neetechs")

    result = verify_get_webauthn_credentials(
        rp=rp,
        challenge_b64=challenge,
        client_data_b64=client_data_b64,
        authenticator_b64=authenticator_data_b64,
        signature_b64=signature_b64,
        sign_count=sign_count,
        pubkey_alg=pubkey_alg,
        pubkey=public_key,
        user_verification_required=True
    )

    return JsonResponse({"status": "ok", "sign_count": result.sign_count})
