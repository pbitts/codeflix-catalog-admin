from rest_framework import serializers

from src.core.castmember.domain.castmember import CastMemberType


class CastMemberTypeField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        # Utilizamos o "choices" do DRF, que permite um conjunto de opções limitado para um certo campo.
        choices = [(type.name, type.value) for type in CastMemberType]
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        # Valor vindo da API como "str" é convertido para o StrEnum
        return CastMemberType(super().to_internal_value(data))

    def to_representation(self, value):
        # O valor vindo do nosso domínio é convertido para uma string na API
        return str(super().to_representation(value))
    
class CastMemberOutputSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField(max_length=255)
    type = CastMemberTypeField()
    
    
class ListCastMemberOutputSerializer(serializers.Serializer):
    data = CastMemberOutputSerializer(many=True)
    
    
class CreateCastMemberInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    type = CastMemberTypeField()
    
    
class CreateCastMemberOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    

class DeleteCastMemberInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class UpdateCastMemberInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    type = CastMemberTypeField()