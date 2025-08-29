from dataclasses import dataclass, field
from uuid import UUID

from src.core.castmember.domain.castmember import CastMember, CastMemberType
from src.core.castmember.application.exceptions import InvalidCastMember, InvalidCastMemberType


class CreateCastMember:
    def __init__(self, repository):
        self.repository = repository
        
    @dataclass
    class Input:
        name: str
        type: CastMemberType
    
    @dataclass
    class Output:
        id: UUID
        
    def execute(self, input: Input):
        if input.type not in[CastMemberType.ACTOR, CastMemberType.DIRECTOR]:
            raise InvalidCastMemberType("Type must be either 'ACTOR' or 'DIRECTOR'")
        
        try:
            castmember = CastMember(
                name=input.name,
                type=input.type
            )
        except ValueError as e:
            raise InvalidCastMember(str(e))
        
        self.repository.save(castmember)
        return self.Output(id=castmember.id)
        
        