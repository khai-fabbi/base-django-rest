from rest_framework import serializers

from apps.api.models.todo import Todo, TodoStatusChoices
from libs.rest_framework.fields import CharField, ChoiceField
from libs.rest_framework.serializers import OnlyOneErrorMixin


class TodoSerializer(OnlyOneErrorMixin, serializers.ModelSerializer):
    name = CharField(max_length=256)
    status = ChoiceField(choices=TodoStatusChoices.choices, required=False)

    class Meta:
        model = Todo
        fields = '__all__'
