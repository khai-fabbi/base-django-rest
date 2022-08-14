from rest_framework import serializers


class TokenRevokeSerializer(serializers.Serializer):
    refresh = serializers.CharField()
