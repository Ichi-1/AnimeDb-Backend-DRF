from rest_framework import serializers


class GoogleAuthSerializer(serializers.Serializer):
    id_token = serializers.CharField()
