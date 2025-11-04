# Neetechs/settings.py
"""
Compatibility shim so Django and tooling that still import 'Neetechs.settings'
will load the correct env-specific settings from Neetechs/settings/*.py
"""

import os
import importlib

# If DJANGO_SETTINGS_MODULE already points to a sub-file, use it.
# Otherwise default to production.
_target = os.getenv("DJANGO_SETTINGS_MODULE", "Neetechs.settings.prod")

# Some tools set DJANGO_SETTINGS_MODULE="Neetechs.settings".
# In that case, force prod.
if _target.rstrip(".py") in {"Neetechs.settings", "settings"}:
    _target = "Neetechs.settings.prod"

# Import the target module and copy ALL-CAPS names into this module's globals.
_mod = importlib.import_module(_target)
for _k, _v in _mod.__dict__.items():
    if _k.isupper():
        globals()[_k] = _v

# Enforce read-only defaults unless a sub-settings module overrides them explicitly.
REST_FRAMEWORK = {
    **globals().get("REST_FRAMEWORK", {}),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly"
    ],
}

# Ensure DRF exposes versioned URLs everywhere.
REST_FRAMEWORK.update(
    {
        "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
        "DEFAULT_VERSION": "v1",
        "ALLOWED_VERSIONS": ("v1",),
    }
)

APPEND_SLASH = True

SPECTACULAR_SETTINGS = {
    "TITLE": "Neetechs API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "COMPONENT_NO_READ_ONLY_REQUIRED": True,
    "ENUM_NAME_OVERRIDES": {"status": "ServiceOrderStatus"},
    "COMPONENT_NAME_OVERRIDES": {
        # disambiguate duplicate Category serializers
        "Category": "CategoryPublic",
    },
    "PREPROCESSING_HOOKS": [],
}

# Optional: make it easy to see which settings loaded when DEBUG is on
if globals().get("DEBUG"):
    loaded_from = _target
    print(f"[Neetechs] Loaded settings from: {loaded_from}")
