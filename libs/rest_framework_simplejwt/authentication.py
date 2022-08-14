from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        """Run authentication and return the authenticated user.
        The access token in the cookie has a higher priority than the one in the header.
        """

        raw_token = request.COOKIES.get(settings.SIMPLE_JWT['ACCESS_TOKEN_COOKIE']) or None

        if raw_token is None:
            header = self.get_header(request)

            if header is not None:
                raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token
