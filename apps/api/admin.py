from django.contrib import admin

from apps.api.models import Action, Category, Post, ProductComment, Rating, Tag, Todo

# Register your models here.


class TodoAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "name",
        "status",
    )
    ordering = ("pk",)
    fields = ("name", "status")


admin.site.register(Todo, TodoAdmin)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Rating)
admin.site.register(ProductComment)
admin.site.register(Tag)
admin.site.register(Action)
