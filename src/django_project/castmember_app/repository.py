from uuid import UUID
from django.db import transaction

from src.core.castmember.domain.castmember import CastMember
from src.core.castmember.domain.castmember_repository import CastMemberRepository
from src.django_project.castmember_app.models import CastMember as CastMemberModel

class DjangoORMCastMemberRepository(CastMemberRepository):
    
    def save(self, castmember: CastMember):
        castmember_orm = CastMemberModelMapper.to_model(castmember)
        castmember_orm.save()
        # with transaction.atomic():
        #     castmember_model = CastMemberModel.objects.create(
        #         id=castmember.id,
        #         name=castmember.name,
        #         type=castmember.type,
        #     )
    
    def get_by_id(self, id: UUID) -> CastMember:
        try:
            castmember_model = CastMemberModel.objects.get(id=id)
            return CastMemberModelMapper.to_entity(castmember_model)
        except CastMemberModel.DoesNotExist:
            return None
        # return CastMember(
        #     id=castmember_model.id,
        #     name=castmember_model.name,
        #     type=castmember_model.type
        # )
    
    def list(self) -> list[CastMember]:
        return [
            CastMemberModelMapper.to_entity(castmember_model)
            for castmember_model in CastMemberModel.objects.all()
        ]
        # return [
        #     CastMember(
        #         id=castmember_model.id,
        #         name=castmember_model.name,
        #         type=castmember_model.type
        #     )
        #     for castmember_model in CastMemberModel.objects.all()
        # ]
    
    def update(self, castmember: CastMember) -> None:
        try:
            castmember_model = CastMemberModel.objects.get(id=castmember.id)
        except CastMemberModel.DoesNotExist:
            return None
        
        with transaction.atomic():
            CastMemberModel.objects.filter(id=castmember.id).update(
                name=castmember.name,
                type=castmember.type,
            )
    
    def delete(self, id: UUID) -> None:
        CastMemberModel.objects.filter(id=id).delete()
        
class CastMemberModelMapper:
    @staticmethod
    def to_model(castmember: CastMember) -> CastMemberModel:
        return CastMemberModel(
            id=castmember.id,
            name=castmember.name,
            type=castmember.type,
            )
    
    @staticmethod
    def to_entity(castmember_model: CastMemberModel) -> CastMember:
            return CastMember(
            id=castmember_model.id,
            name=castmember_model.name,
            type=castmember_model.type
        )