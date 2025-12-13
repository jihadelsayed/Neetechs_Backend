from corsheaders.defaults import default_headers
from decouple import config

CORS_ALLOW_HEADERS = list(default_headers) + ["x-device-id"]
CORS_ALLOW_CREDENTIALS = True
# Optional: CORS_ALLOWED_ORIGINS via .env if you want a whitelist:
# from decouple import config
# CORS_ALLOWED_ORIGINS = [s.strip() for s in config("CORS_ALLOWED_ORIGINS", default="").split(",") if s.strip()]


# Allow ANY subdomain of neetechs.com (accounts.neetechs.com, myaccount.neetechs.com, etc.)
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://([a-z0-9-]+\.)*neetechs\.com$",
    r"^https://([a-z0-9-]+\.)*theislamicnation\.com$",
    r"^https://([a-z0-9-]+\.)*nelingo\.com$",
]

    # s.strip()
    # for s in config("CORS_ALLOWED_ORIGINS", default="").split(",")
    # if s.strip()
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "https://neetechs.com",
    "https://server.neetechs.com",
      "https://accounts.neetechs.com",
  "https://accounts.theislamicnation.com",

    "https://theislamicnation.com",
    "https://neetechpanel.asuscomm.com"

]
CSRF_TRUSTED_ORIGINS = [
  "https://neetechs.com",
  "https://server.neetechs.com",
  "https://accounts.neetechs.com",
  "https://accounts.theislamicnation.com",
      "https://theislamicnation.com",
    "https://neetechpanel.asuscomm.com"
]
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

WEBAUTHN_ENABLED = False
WEBAUTHN_RP_ID = "neetechs.com"
WEBAUTHN_RP_NAME = "Neetechs"
TWILIO_OTP_MESSAGE_TEMPLATE = "🔐 Your Neetechs verification code is: {code}"


ACCOUNT_ADAPTER = "accounts.adapters.AccountAdapter"
#FRONTEND_URL = "http://localhost:4200"  # dev
FRONTEND_URL = "https://neetechs.com"  # prod
