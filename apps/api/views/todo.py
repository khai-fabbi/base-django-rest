
import logging

from rest_framework import generics, status
from rest_framework.permissions import BasePermission, DjangoModelPermissions, DjangoObjectPermissions, IsAdminUser
from rest_framework.response import Response

from apps.api.models.todo import Todo
from apps.api.serializers.todo_serializer import TodoSerializer
from helpers.permissions import IsSuperAdmin
from libs.rest_framework.renderers import JSONRenderer

logger = logging.getLogger()


class HasAllTodoPermissions(BasePermission):
    message = 'All actions with Todo are not allowed.'

    def has_permission(self, request, view):
        return request.user.has_perm('api.view_todo')


class TodoList(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    # permission_classes = [HasAllTodoPermissions | IsSuperAdmin]
    permission_classes = [DjangoModelPermissions]
    filterset_fields = ['name', 'status']
    search_fields = ['name']
    # ordering_fields = ['id']  # '__all__'
    ordering = ['id']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as exc:
            logger.info(serializer.initial_data)
            logger.warning(exc)
            raise exc


class TodoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [DjangoModelPermissions]
