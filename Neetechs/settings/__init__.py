# Compose settings from parts; Django imports this module.
from .core import *              # BASE_DIR, DEBUG, paths, static/media, i18n
from .apps import *              # INSTALLED_APPS
from .middleware import *        # MIDDLEWARE
from .templates import *         # TEMPLATES
from .auth import *              # AUTH_USER_MODEL, AUTHENTICATION_BACKENDS, allauth
from .rest import *              # DRF, Spectacular, Knox
from .cors import *              # CORS_*
from .db import *                # DATABASES
from .channels_settings import * # CHANNEL_LAYERS
from .email_settings import *    # EMAIL_*
from .storage import *           # S3 / storages
from .third_party import *       # Stripe/Twilio/etc.
import warnings

# Optional logging (keep your existing file)
try:
    from Neetechs.logging_config import LOGGING  # noqa
except Exception:
    LOGGING = {}
warnings.filterwarnings(
    "ignore",
    message=r"app_settings\.(USERNAME_REQUIRED|EMAIL_REQUIRED) is deprecated",
    module=r"dj_rest_auth\.registration\.serializers",
)