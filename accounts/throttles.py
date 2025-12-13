from rest_framework.throttling import SimpleRateThrottle

class LoginThrottle(SimpleRateThrottle):
    scope = "login"

    def get_cache_key(self, request, view):
        # Prefer user/email/phone target when present, fall back to IP.
        ident = (
            request.data.get("email")
            or request.data.get("phone")
            or self.get_ident(request)
        )
        return f"throttle_login_{ident}".lower()


class RegisterThrottle(SimpleRateThrottle):
    scope = "register"

    def get_cache_key(self, request, view):
        ident = (
            request.data.get("email")
            or request.data.get("phone")
            or self.get_ident(request)
        )
        return f"throttle_register_{ident}".lower()


class OTPThrottle(SimpleRateThrottle):
    scope = "otp"

    def get_cache_key(self, request, view):
        # OTP should be keyed primarily on phone, else IP.
        ident = request.data.get("phone") or self.get_ident(request)
        return f"throttle_otp_{ident}".lower()
