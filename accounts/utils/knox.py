from knox.models import AuthToken
 

def create_knox_token(token_model, user, serializer):
    """
    Compatibility hook used by dj-rest-auth/knox integration.
    Signature stays as-is, but we intentionally ignore token_model/serializer.
    """
    _, token = AuthToken.objects.create(user)
    return token