from rest_framework import viewsets, status, exceptions
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from apps.api.serializers.blog_serializer import *
from ..exceptions import CategoryExeption, PageNotFound
from ..pagination import BlogPaginator


class CategoryViewSet(viewsets.ViewSet, generics.ListCreateAPIView, ):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_active=True)
    # pagination_class = BlogPaginator

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        category_list = Category.objects.filter(is_active=True)
        name_category = self.request.query_params.get('name')
        if name_category:
            category_list = category_list.filter(name__icontains=name_category)
        return category_list

    def retrieve(self, request, pk=None):
        try:
            id_cate = int(pk)
        except ValueError or IndexError:
            raise exceptions.APIException('Sai dinh dang id',status.HTTP_400_BAD_REQUEST)
        try:
            category = Category.objects.get(pk=id_cate, is_active=True)
        except Category.DoesNotExist:
            raise exceptions.APIException( 'Khong tim thay danh muc',status.HTTP_404_NOT_FOUND)
        else:
            serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
