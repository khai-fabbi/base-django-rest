from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser
from apps.api.serializers.user_serializer import UserSerializer
from apps.authen.models import *
class UserViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)
    permission_classes = [AllowAny,]
    pagination_class = None

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]