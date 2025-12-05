
from typing import Optional
import logging

from django.conf import settings
from twilio.rest import Client

logger = logging.getLogger(__name__)


def send_sms_otp(to_phone: str, otp_code: str) -> Optional[str]:
    """
    Sends a verification code via SMS using Twilio.
    Returns the message SID if sent successfully, otherwise None.
    """
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"🔐 Your Neetechs verification code is: {otp_code}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to_phone,
        )
        logger.info("Twilio SMS sent to %s (SID=%s)", to_phone, message.sid)
        return message.sid
    except Exception as e:
        logger.error("Failed to send OTP to %s: %s", to_phone, e)
        return None
