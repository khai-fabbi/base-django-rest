from django.db import models


class TodoStatusChoices(models.TextChoices):
    NOT_STARTED = 'not_started'
    DOING = 'doing'
    DONE = 'done'


class Todo(models.Model):
    name = models.CharField(max_length=256)
    status = models.CharField(max_length=32, choices=TodoStatusChoices.choices, default=TodoStatusChoices.NOT_STARTED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_todo'
