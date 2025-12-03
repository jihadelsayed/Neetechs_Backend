from decouple import config
from storages.backends.s3boto3 import S3Boto3Storage

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default="")
AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME", default="us-east-1")

AWS_STATIC_BUCKET_NAME = config("AWS_STATIC_BUCKET_NAME")
AWS_PRODUCTS_BUCKET_NAME = config("AWS_PRODUCTS_BUCKET_NAME")
AWS_UPLOADS_BUCKET_NAME = config("AWS_UPLOADS_BUCKET_NAME")

AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=604800",
}

# Match "ACLs disabled" on the buckets
AWS_DEFAULT_ACL = None


class StaticStorage(S3Boto3Storage):
    bucket_name = AWS_STATIC_BUCKET_NAME
    default_acl = None
    location = ""
    custom_domain = f"{bucket_name}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"


class UploadsStorage(S3Boto3Storage):
    bucket_name = AWS_UPLOADS_BUCKET_NAME
    default_acl = None
    location = ""
    custom_domain = f"cdn.neetechs.com"


class ProductsStorage(S3Boto3Storage):
    bucket_name = AWS_PRODUCTS_BUCKET_NAME
    default_acl = None
    location = ""
    custom_domain = f"{bucket_name}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"


if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
    # Django 5+ prefers STORAGES – make static+default use our S3 backends
    STORAGES = {
        "default": {
            "BACKEND": "Neetechs.settings.storage.UploadsStorage",
        },
        "staticfiles": {
            "BACKEND": "Neetechs.settings.storage.StaticStorage",
        },
    }

    # Keep these too for compatibility
    DEFAULT_FILE_STORAGE = "Neetechs.settings.storage.UploadsStorage"
    STATICFILES_STORAGE = "Neetechs.settings.storage.StaticStorage"
