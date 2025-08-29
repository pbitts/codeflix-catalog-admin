from dataclasses import dataclass
from uuid import UUID

from src.core.castmember.application.exceptions import CastMemberNotFound, InvalidCastMember, InvalidCastMemberType
from src.core.castmember.domain.castmember import CastMemberType
from src.core.castmember.domain.castmember_repository import CastMemberRepository


    
class UpdateCastMember:
    
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository
        
    @dataclass
    class Input:
        id: UUID
        name: str
        type: CastMemberType

    def execute(self, input: Input) -> None:
        castmember = self.repository.get_by_id(input.id)
        if not castmember:
            raise CastMemberNotFound(f"CastMember with id {input.id} not found")
        
        try:    
            castmember.change_name(name=input.name)
        except ValueError as err:
            raise InvalidCastMember(err)
        
        try:    
            castmember.update_type(type=input.type)
        except ValueError as err:
            raise InvalidCastMemberType(err)

        self.repository.update(castmember)
        
        