from django.conf import settings
from django.urls import path

from apps.authen.views.jwt_view import CustomTokenObtainPairView, CustomTokenRefreshView, TokenRevokeView

urlpatterns = [
    path(settings.SIMPLE_JWT['TOKEN_ENDPOINT'] + 'generate/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(settings.SIMPLE_JWT['TOKEN_ENDPOINT'] + 'refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path(settings.SIMPLE_JWT['TOKEN_ENDPOINT'] + 'revoke/', TokenRevokeView.as_view(), name='token_revoke'),
]
