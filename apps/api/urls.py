from django.urls import path,include
from apps.api.views.todo import TodoDetail, TodoList
from rest_framework.routers import DefaultRouter

from apps.api.views.user_view import UserViewSet
from apps.api.views.blog_view import CategoryViewSet

router = DefaultRouter()
router.register('users',UserViewSet)
router.register('category', CategoryViewSet,)
urlpatterns = [
    path("todos/", TodoList.as_view(), name="todo_list"),
    path("todos/<int:pk>/", TodoDetail.as_view(), name="todo_detail"),
    path('',include(router.urls)),
]
