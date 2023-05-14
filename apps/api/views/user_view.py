from django.http import Http404
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from apps.api.serializers.user_serializer import UserSerializer
from apps.authen.models import *
from rest_framework.response import Response
class UserViewSet(viewsets.ViewSet, generics.RetrieveAPIView, generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated,]
    pagination_class = None

    # def get_permissions(self):
    #     if self.action == 'list':
    #         permission_classes = [AllowAny]
    #     else:
    #         permission_classes = [IsAdminUser]
    #     return [permission() for permission in permission_classes]

class UserCurrentAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self,request):
        try :
            user = request.user
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)