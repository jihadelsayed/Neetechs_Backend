from twilio.rest import Client
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_sms_otp(to_phone: str, otp_code: str) -> str:
    """
    Sends a verification code via SMS using Twilio.
    Returns the message SID if sent successfully.
    """
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"🔐 Your Neetechs verification code is: {otp_code}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to_phone
        )
        logger.info(f"Twilio SMS sent to {to_phone}: SID {message.sid}")
        return message.sid
    except Exception as e:
        logger.error(f"Failed to send OTP to {to_phone}: {e}")
        return ""
