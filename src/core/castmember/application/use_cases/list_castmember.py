

from dataclasses import dataclass
from uuid import UUID

from src.core.castmember.domain.castmember import CastMemberType
from src.core.castmember.domain.castmember_repository import CastMemberRepository


@dataclass
class CastMemberOutput:
    id: UUID
    name: str
    type: CastMemberType

class ListCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository
        
    
    @dataclass
    class Input:
        pass
    
    @dataclass
    class Output:
        data: list[CastMemberOutput]
        
    def execute(self, input: Input) -> Output:
        castmembers = self.repository.list()
        output_data = [
            CastMemberOutput(
                id=castmember.id,
                name=castmember.name,
                type=castmember.type
            ) for castmember in castmembers
        ]
        return self.Output(data=output_data)