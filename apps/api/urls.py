from django.urls import path,include
from rest_framework.routers import DefaultRouter

from apps.api.views.user_view import UserViewSet,UserCurrentAPIView
from apps.api.views.blog_view import CategoryViewSet, PostViewSet

router = DefaultRouter()
router.register('users',UserViewSet)
router.register('category', CategoryViewSet,basename='category')
router.register('post', PostViewSet,basename='post')
urlpatterns = [
    path('',include(router.urls)),
    path('me/', UserCurrentAPIView.as_view()),
]
