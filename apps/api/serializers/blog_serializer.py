from rest_framework import serializers
from ..models import Category, Post, Tag, Rating


class CategorySerializer(serializers.ModelSerializer):
    post_category = serializers.SlugRelatedField(many=True, read_only=True, slug_field='title')

    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'view', 'slug', 'is_hot', 'category', 'author']
        # fields = '__all__'
