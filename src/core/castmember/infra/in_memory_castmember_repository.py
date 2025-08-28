from uuid import UUID

from src.core.castmember.domain.castmember_repository import CastMemberRepository
from src.core.castmember.domain.castmember import CastMember


class InMemoryCastMemberRepository(CastMemberRepository):
    def __init__(self, castmembers=None):
        self.castmembers = castmembers or []
    
    def save(self, castmember):
        self.castmembers.append(castmember)
    
    def get_by_id(self, id: UUID) -> CastMember | None:
        return next((castmember for castmember in self.castmembers if castmember.id == id), None)
    
    def delete(self, id: UUID) -> None:
        castmember = self.get_by_id(id)
        self.castmembers.remove(castmember)
    
    def update(self, castmember: CastMember) -> None:
        old_castmember = self.get_by_id(castmember.id) 
        if castmember:
            self.castmembers.remove(castmember)
            self.castmembers.append(castmember)
    
    def list(self) -> list[CastMember]:
        # Return a copy of the castmembera list to avoid external modifications
        return [castmember for castmember in self.castmembers]