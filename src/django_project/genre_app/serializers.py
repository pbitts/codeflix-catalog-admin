from rest_framework import serializers

from src.django_project._shared.serializers import ListOutputMetaSerializer


class GenreOutputSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField()
    categories = serializers.ListField(child=serializers.CharField())
    
class ListGenreOutputSerializer(serializers.Serializer):
    data = GenreOutputSerializer(many=True)
    meta = ListOutputMetaSerializer()
    
class SetField(serializers.ListField):
    # Outras alternativas:
    # Na view, converter para set manualmente
    # Utilizar o SerializerMethodField
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))
    def to_representation(self, value):
        return list(super().to_representation(value))
    
class CreateGenreInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField(default=True)
    categories = SetField(child=serializers.UUIDField())
    

class CreateGenreOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    

class DeleteGenreInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class UpdateGenreInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField(default=True)
    categories = SetField(child=serializers.UUIDField())