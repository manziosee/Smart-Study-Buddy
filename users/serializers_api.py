from rest_framework import serializers

class LogoutResponseSerializer(serializers.Serializer):
    message = serializers.CharField()