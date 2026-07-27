import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None
        try:
            prefix, token = auth_header.split(" ")
        except ValueError:
            raise AuthenticationFailed("Invalid Authorization header format")

        if prefix.lower() != "bearer":
            raise AuthenticationFailed("Authorization header must start with Bearer")
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        return (payload, token)