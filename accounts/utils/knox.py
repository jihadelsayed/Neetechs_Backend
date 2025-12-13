 

from knox.models import AuthToken

def create_knox_token(user):
    _, token = AuthToken.objects.create(user)
    return token

