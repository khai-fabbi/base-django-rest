from django_filters import FilterSet, CharFilter
from .models import Post, Category


class PostFilter(FilterSet):
    keyword = CharFilter(field_name='title', lookup_expr='icontains')
    slug = CharFilter(field_name='slug', lookup_expr='exact')
    author = CharFilter(field_name='author__first_name', lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ['title', 'slug', 'author']
