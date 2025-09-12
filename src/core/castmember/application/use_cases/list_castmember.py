

from dataclasses import dataclass, field
from uuid import UUID

from src.core._shared.meta import ListOutputMeta
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
        order_by : str = "name"
        current_page: int = 1
    
    @dataclass
    class Output:
        data: list[CastMemberOutput]
        meta: ListOutputMeta = field(default_factory=ListOutputMeta)
        
    def execute(self, input: Input) -> Output:
        cast_members = self.repository.list()
        
        
        output_data = [
            CastMemberOutput(
                id=castmember.id,
                name=castmember.name,
                type=castmember.type
            ) for castmember in cast_members
        ]
        
        
        sorted_cast_members = sorted([
                            CastMemberOutput(
                id=castmember.id,
                name=castmember.name,
                type=castmember.type
            ) for castmember in cast_members
                        ],
            key=lambda castmember: getattr(castmember, input.order_by))
        
        DEFAULT_PAGE_SIZE = 2
        page_offset = (input.current_page - 1) * DEFAULT_PAGE_SIZE
        castmember_page = sorted_cast_members[page_offset:page_offset + DEFAULT_PAGE_SIZE]
        
        return self.Output(
            data=castmember_page,
            meta=(ListOutputMeta(
                current_page=input.current_page,
                per_page=DEFAULT_PAGE_SIZE,
                total=len(sorted_cast_members)
            ))
        )