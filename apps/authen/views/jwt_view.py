import logging
from typing import Optional

from django.conf import settings
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from libs.rest_framework_simplejwt.serializers import TokenRevokeSerializer

logger = logging.getLogger()


class SetTokenToCookie:
    """Set access token and refresh token to cookie."""

    def set_cookie(self, response: Response, access_token: str, refresh_token: Optional[str]) -> None:
        current_time = timezone.now()

        response.set_cookie(key=settings.SIMPLE_JWT['ACCESS_TOKEN_COOKIE'],
                            value=access_token,
                            path='/',
                            expires=current_time + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                            secure=settings.SIMPLE_JWT['COOKIE_SECURE'],
                            httponly=settings.SIMPLE_JWT['COOKIE_HTTP_ONLY'],
                            samesite=settings.SIMPLE_JWT['COOKIE_SAMESITE'],
                            )

        if refresh_token is not None:
            response.set_cookie(key=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE'],
                                value=refresh_token,
                                path='/' + settings.API_ENTRY_POINT + settings.SIMPLE_JWT['TOKEN_ENDPOINT'],
                                expires=current_time + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                                secure=settings.SIMPLE_JWT['COOKIE_SECURE'],
                                httponly=settings.SIMPLE_JWT['COOKIE_HTTP_ONLY'],
                                samesite=settings.SIMPLE_JWT['COOKIE_SAMESITE'],
                                )


class CustomTokenObtainPairView(SetTokenToCookie, TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)

        self.set_cookie(response,
                        serializer.validated_data.get('access'),
                        serializer.validated_data.get('refresh'))

        return response


class CustomTokenRefreshView(SetTokenToCookie, TokenRefreshView):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """

    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE']) or request.data.get('refresh')

        serializer = self.get_serializer(data={'refresh': refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)

        self.set_cookie(response,
                        serializer.validated_data.get('access'),
                        serializer.validated_data.get('refresh'))

        return response


class TokenRevokeView(generics.GenericAPIView):
    """Revoke token."""

    serializer_class = TokenRevokeSerializer

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE']) or request.data.get('refresh')

        serializer = self.get_serializer(data={'refresh': refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        refresh = RefreshToken(serializer.validated_data.get('refresh'))
        try:
            # Attempt to blacklist the given refresh token
            refresh.blacklist()
        except AttributeError:
            # If blacklist app not installed, `blacklist` method will
            # not be present
            pass

        response = Response(status=status.HTTP_200_OK)

        response.delete_cookie(key=settings.SIMPLE_JWT['ACCESS_TOKEN_COOKIE'], path='/')
        response.delete_cookie(key=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE'],
                               path='/' + settings.API_ENTRY_POINT + settings.SIMPLE_JWT['TOKEN_ENDPOINT'])

        return response
