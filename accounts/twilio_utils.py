from typing import Optional
import logging

from django.conf import settings
from twilio.rest import Client

logger = logging.getLogger(__name__)

_client: Optional[Client] = None


def _get_client() -> Client:
    global _client
    if _client is None:
        _client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    return _client


def _mask_phone(phone: str) -> str:
    p = (phone or "").strip()
    if len(p) <= 4:
        return "***"
    return f"***{p[-4:]}"


def send_sms_otp(to_phone: str, otp_code: str) -> Optional[str]:
    """
    Sends a verification code via SMS using Twilio.
    Returns the message SID if sent successfully, otherwise None.
    """
    to_phone = (to_phone or "").strip()
    otp_code = (otp_code or "").strip()

    if not to_phone or not otp_code:
        return None

    try:
        body = getattr(
            settings,
            "TWILIO_OTP_MESSAGE_TEMPLATE",
            "Your Neetechs verification code is: {code}",
        ).format(code=otp_code)

        client = _get_client()
        message = client.messages.create(
            body=body,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to_phone,
        )

        logger.info("Twilio SMS sent to %s (SID=%s)", _mask_phone(to_phone), message.sid)
        return message.sid

    except Exception:
        logger.exception("Failed to send OTP to %s", _mask_phone(to_phone))
        return None
