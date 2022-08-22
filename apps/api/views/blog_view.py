from builtins import filter

from rest_framework import viewsets, status, exceptions
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Post, Category, User, Tag, Rating, ProductComment
from apps.api.serializers.blog_serializer import *
from ..exceptions import CategoryExeption, PageNotFound
from ..pagination import BlogPaginator
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from ..filters import PostFilter


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
            raise exceptions.APIException('Sai dinh dang id', status.HTTP_400_BAD_REQUEST)
        try:
            category = Category.objects.get(pk=id_cate, is_active=True)
        except Category.DoesNotExist:
            raise exceptions.APIException('Khong tim thay danh muc', status.HTTP_404_NOT_FOUND)
        else:
            serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostViewSet(viewsets.ViewSet, generics.ListCreateAPIView, generics.RetrieveAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.select_related('category').select_related('author').filter(is_active=True)
    permission_classes = [AllowAny, ]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

    def get_queryset(self):
        post_list = Post.objects.select_related('category').select_related('author').filter(is_active=True)
        name_post = self.request.query_params.get('name')
        if name_post:
            post_list = post_list.filter(name__icontains=name_post)
        return post_list

    def retrieve(self, request, slug=None):
        # print(pk)
        # try:
        #     id_post = int(pk)
        # except ValueError or IndexError:
        #     raise exceptions.APIException('Sai dinh dang id',status.HTTP_400_BAD_REQUEST)
        # try:
        #     post = Post.objects.get(pk=id_post, is_active=True)
        # except Post.DoesNotExist:
        #     raise exceptions.APIException( 'Khong tim thay bai viet',status.HTTP_404_NOT_FOUND)
        # else:
        #     serializer = PostSerializer(post)
        try:
            post = Post.objects.get(slug__exact=slug)
        except Post.DoesNotExist:
            raise exceptions.APIException('Khong tim thay slug', status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

