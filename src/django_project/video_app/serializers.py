from django.forms import UUIDField
from django.forms import DecimalField
from rest_framework import serializers


class SetField(serializers.ListField):
    # Outras alternativas:
    # Na view, converter para set manualmente
    # Utilizar o SerializerMethodField
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))
    def to_representation(self, value):
        return list(super().to_representation(value))
    
class CreateVideoInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    launch_year = serializers.IntegerField()
    duration = serializers.IntegerField()
    opened = serializers.BooleanField(default=False)
    rating = serializers.CharField(max_length=10)
    categories = SetField(child=serializers.UUIDField())
    genres = SetField(child=serializers.UUIDField())
    cast_members = SetField(child=serializers.UUIDField())


class CreateVideoOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()