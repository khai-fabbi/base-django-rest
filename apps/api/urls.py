from django.urls import path
from apps.api.views.todo import TodoDetail, TodoList

urlpatterns = [
    path("todos/", TodoList.as_view(), name="todo_list"),
    path("todos/<int:pk>/", TodoDetail.as_view(), name="todo_detail"),
]
