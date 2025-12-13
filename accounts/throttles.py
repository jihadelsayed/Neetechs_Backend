from rest_framework.throttling import SimpleRateThrottle


def _norm(v: str | None) -> str | None:
    if v is None:
        return None
    v = str(v).strip().lower()
    return v or None


def _get_target(request) -> str | None:
    # Safe access even if request.data isn't normal
    try:
        data = request.data or {}
    except Exception:
        data = {}

    email = _norm(getattr(data, "get", lambda _k, _d=None: None)("email"))
    phone = _norm(getattr(data, "get", lambda _k, _d=None: None)("phone"))
    return email or phone


class LoginThrottle(SimpleRateThrottle):
    scope = "login"

    def get_cache_key(self, request, view):
        ip = self.get_ident(request)
        target = _get_target(request)

        # throttle by (target + ip) when target exists, else just ip
        ident = f"{target}:{ip}" if target else ip
        return self.cache_format % {"scope": self.scope, "ident": ident}


class RegisterThrottle(SimpleRateThrottle):
    scope = "register"

    def get_cache_key(self, request, view):
        ip = self.get_ident(request)
        target = _get_target(request)

        ident = f"{target}:{ip}" if target else ip
        return self.cache_format % {"scope": self.scope, "ident": ident}


class OTPThrottle(SimpleRateThrottle):
    scope = "otp"

    def get_cache_key(self, request, view):
        ip = self.get_ident(request)

        try:
            data = request.data or {}
        except Exception:
            data = {}

        phone = _norm(getattr(data, "get", lambda _k, _d=None: None)("phone"))

        # OTP: primarily by phone, but include IP to reduce shared-phone abuse
        ident = f"{phone}:{ip}" if phone else ip
        return self.cache_format % {"scope": self.scope, "ident": ident}
