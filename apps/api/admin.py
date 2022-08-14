from django.contrib import admin

from apps.api.models.todo import Todo

# Register your models here.


class TodoAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'status',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'name',
        'status',
    )
    ordering = (
        'pk',
    )
    fields = ('name', 'status')


admin.site.register(Todo, TodoAdmin)
