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

# Optional: make it easy to see which settings loaded when DEBUG is on
if globals().get("DEBUG"):
    loaded_from = _target
    print(f"[Neetechs] Loaded settings from: {loaded_from}")
