from unittest.mock import create_autospec
import uuid
import pytest

from core.castmember.application.use_cases.create_castmember import CreateCastMember
from src.core.castmember.domain.castmember import CastMember
from src.core.castmember.domain.castmember_repository import CastMemberRepository
from src.core.castmember.application.exceptions import InvalidCastMember, InvalidCastMemberType


@pytest.fixture
def mock_castmember_repository() -> CastMemberRepository:
    return create_autospec(CastMemberRepository)
    

class TestCreateCastMember:
    def test_create_castmember_with_valid_data(
        self,
        mock_castmember_repository):

        use_case = CreateCastMember(
            repository=mock_castmember_repository,
        )
        input = CreateCastMember.Input(name="Ren", type='ACTOR')
        
        output = use_case.execute(input)
        
        assert isinstance(output.id, uuid.UUID)
        mock_castmember_repository.save.assert_called_once_with(
            CastMember(
                id=output.id,
                name='Ren',
                type='ACTOR'
            )
        )

    def test_create_castmember_invalid_name(
        self,
        mock_castmember_repository
    ):
        use_case = CreateCastMember(
            repository=mock_castmember_repository,
        )
        input = CreateCastMember.Input(name="", type='ACTOR')
        
        with pytest.raises(InvalidCastMember):
            use_case.execute(input)
        
        mock_castmember_repository.save.assert_not_called()
    
    def test_create_castmember_empty_name(
        self,
        mock_castmember_repository
    ):
        use_case = CreateCastMember(
            repository=mock_castmember_repository,
        )
            
        input = CreateCastMember.Input(name="a"*256, type='ACTOR')
        
        with pytest.raises(InvalidCastMember):
            use_case.execute(input)
        
        mock_castmember_repository.save.assert_not_called()
            
    def test_create_castmember_invalid_type(
        self,
        mock_castmember_repository
    ):
        use_case = CreateCastMember(
            repository=mock_castmember_repository,
        )
        
        input = CreateCastMember.Input(name="Albert", type='INVALID')
        
        with pytest.raises(InvalidCastMemberType):
            use_case.execute(input)
        
        mock_castmember_repository.save.assert_not_called()
        
        
        