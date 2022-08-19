from rest_framework import serializers
from django.conf import settings
from apps.authen.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "avatar",
        ]
        app_label = 'user_app'
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ["username"]

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
