
from knox.models import AuthToken


def create_knox_token(token_model, user, serializer):
    _, token = AuthToken.objects.create(user)
    return token
