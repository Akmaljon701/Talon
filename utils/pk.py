from rest_framework import serializers


class PkSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
