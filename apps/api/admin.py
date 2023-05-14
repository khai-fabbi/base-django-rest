from django.contrib import admin

from apps.api.models import Action, Category, Post, ProductComment, Rating, Tag

# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Rating)
admin.site.register(ProductComment)
admin.site.register(Tag)
admin.site.register(Action)
