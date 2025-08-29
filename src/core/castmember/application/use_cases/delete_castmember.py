from dataclasses import dataclass
from uuid import UUID

from src.core.castmember.application.exceptions import CastMemberNotFound
from src.core.castmember.domain.castmember_repository import CastMemberRepository


class DeleteCastMember:
    
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository
        
    @dataclass
    class Input:
        id: UUID

    def execute(self, input: Input) -> None:
        castmember = self.repository.get_by_id(input.id)

        if not castmember:
            raise CastMemberNotFound(f"CastMember with id {input.id} not found")

        self.repository.delete(castmember.id)