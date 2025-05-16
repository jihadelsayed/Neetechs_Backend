# knox_allauth/views_set_password.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class SetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        password = request.data.get("password")
        if not password or len(password) < 6:
            return Response({"detail": "Password too short."}, status=400)

        user = request.user
        user.set_password(password)
        user.save()

        return Response({"detail": "Password set successfully."}, status=200)
