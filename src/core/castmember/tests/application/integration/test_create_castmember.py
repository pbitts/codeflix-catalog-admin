import uuid
import pytest

from src.core.castmember.application.exceptions import InvalidCastMemberType
from src.core.castmember.application.use_cases.create_castmember import CreateCastMember
from src.core.castmember.infra.in_memory_castmember_repository import InMemoryCastMemberRepository



class TestCreateCastMember:
    def test_create_castmember(
        self
    ):
        castmember_repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(
            repository=castmember_repository
        )
        input = CreateCastMember.Input(
            name="Albert",
            type='ACTOR'
        )
        
        output = use_case.execute(input)
        
        assert isinstance(output, CreateCastMember.Output)
        assert isinstance(output.id, uuid.UUID)
        assert len(castmember_repository.castmembers) == 1
        castmembers = castmember_repository.get_by_id(output.id)
        assert castmembers.id == output.id
        assert castmembers.name == "Albert"
        assert castmembers.type == 'ACTOR'
    
    def test_create_castmember_with_invalid_type(
        self,
    ):
        castmember_repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(
            repository=castmember_repository
        )
        input = CreateCastMember.Input(
            name="Albert",
            type='INVALID'
        )
        
        with pytest.raises(InvalidCastMemberType) as exc_info:
            use_case.execute(input)
        
        assert len(castmember_repository.castmembers) == 0
        