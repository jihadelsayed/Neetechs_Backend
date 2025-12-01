from corsheaders.defaults import default_headers
from networkx import config
CORS_ALLOW_HEADERS = list(default_headers) + ["x-device-id"]
CORS_ALLOW_CREDENTIALS = True
# Optional: CORS_ALLOWED_ORIGINS via .env if you want a whitelist:
# from decouple import config
# CORS_ALLOWED_ORIGINS = [s.strip() for s in config("CORS_ALLOWED_ORIGINS", default="").split(",") if s.strip()]
 
CORS_ALLOWED_ORIGINS = [
    s.strip()
    for s in config("CORS_ALLOWED_ORIGINS", default="").split(",")
    if s.strip()
]
