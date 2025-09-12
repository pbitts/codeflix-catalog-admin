from uuid import UUID

from src.core.castmember.domain.castmember_repository import CastMemberRepository
from src.core.castmember.domain.castmember import CastMember


class InMemoryCastMemberRepository(CastMemberRepository):
    def __init__(self, cast_members=None):
        self.cast_members = cast_members or []
    
    def save(self, castmember):
        self.cast_members.append(castmember)
    
    def get_by_id(self, id: UUID) -> CastMember | None:
        return next((castmember for castmember in self.cast_members if castmember.id == id), None)
    
    def delete(self, id: UUID) -> None:
        castmember = self.get_by_id(id)
        self.cast_members.remove(castmember)
    
    def update(self, castmember: CastMember) -> None:
        old_castmember = self.get_by_id(castmember.id) 
        if castmember:
            self.cast_members.remove(castmember)
            self.cast_members.append(castmember)
    
    def list(self) -> list[CastMember]:
        # Return a copy of the castmembera list to avoid external modifications
        return [castmember for castmember in self.cast_members]