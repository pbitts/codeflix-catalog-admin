from uuid import UUID
from django.db import transaction

from src.core.castmember.domain.castmember import CastMember
from src.core.castmember.domain.castmember_repository import CastMemberRepository
from src.django_project.castmember_app.models import CastMember as CastMemberModel

class DjangoORMCastMemberRepository(CastMemberRepository):
    
    def save(self, castmember: CastMember):
        with transaction.atomic():
            castmember_model = CastMemberModel.objects.create(
                id=castmember.id,
                name=castmember.name,
                type=castmember.type,
            )
    
    def get_by_id(self, id: UUID) -> CastMember:
        try:
            castmember_model = CastMemberModel.objects.get(id=id)
        except CastMemberModel.DoesNotExist:
            return None
        return CastMemberModel(
            id=castmember_model.id,
            name=castmember_model.name,
            type=castmember_model.type
        )
    
    def list(self) -> list[CastMember]:
        return [
            CastMember(
                id=castmember_model.id,
                name=castmember_model.name,
                type=castmember_model.type
            )
            for castmember_model in CastMemberModel.objects.all()
        ]
    
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