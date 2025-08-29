from unittest.mock import create_autospec
from uuid import uuid4

import pytest

from src.core.castmember.application.exceptions import CastMemberNotFound, InvalidCastMember, InvalidCastMemberType
from src.core.castmember.application.use_cases.update_castmember import UpdateCastMember
from src.core.castmember.domain.castmember import CastMember
from src.core.castmember.domain.castmember_repository import CastMemberRepository


@pytest.fixture
def mock_castmember_repository() -> CastMemberRepository:
    return create_autospec(CastMemberRepository)

        
class TestUpdateCastMember:
    def test_update_non_existent_castmember_raises_castmember_not_found(
        self,
        mock_castmember_repository: CastMemberRepository
    ):
        
        mock_castmember_repository.get_by_id.return_value = None
        
        use_case = UpdateCastMember(
            repository=mock_castmember_repository
        )
        
        fake_id = uuid4()
        with pytest.raises(CastMemberNotFound):
            use_case.execute(input=UpdateCastMember.Input(id=fake_id, name='John', type='ACTOR'))
        
        mock_castmember_repository.get_by_id.assert_called_once_with(fake_id)
    
    def test_update_castmember_with_invalid_data_raises_invalid_genre(
        self,
        mock_castmember_repository: CastMemberRepository
    ):
        
        existing_castmember = CastMember(name="Antony", type='DIRECTOR')
        
        mock_castmember_repository.get_by_id.return_value = existing_castmember
        
        use_case = UpdateCastMember(
            repository=mock_castmember_repository
        )
        
        with pytest.raises(InvalidCastMember):
            use_case.execute(input=UpdateCastMember.Input(
                id=existing_castmember.id,
                name="",  # Invalid name
                type='DIRECTOR'
            ))
        
        mock_castmember_repository.get_by_id.assert_called_once_with(existing_castmember.id)
        mock_castmember_repository.update.assert_not_called()
        
    def test_update_castmember_with_invalid_type_raise_invalidcastmembertype(
        self,
        mock_castmember_repository: CastMemberRepository
    ):
        
        existing_castmember = CastMember(name="Alf", type='DIRECTOR')
        
        mock_castmember_repository.get_by_id.return_value = existing_castmember
        
        use_case = UpdateCastMember(
            repository=mock_castmember_repository
        )
        
        with pytest.raises(InvalidCastMemberType):
            use_case.execute(input=UpdateCastMember.Input(
                id=existing_castmember.id,
                name="Alf",
                type='E.T'
            ))
        
        mock_castmember_repository.get_by_id.assert_called_once_with(existing_castmember.id)
        mock_castmember_repository.update.assert_not_called()
    
    def test_successful_castmember_update(
        self,
        mock_castmember_repository: CastMemberRepository
    ):
        
        existing_castmember = CastMember(name="Alf", type='ACTOR')
        
        mock_castmember_repository.get_by_id.return_value = existing_castmember
        
        use_case = UpdateCastMember(
            repository=mock_castmember_repository
        )
        
        new_name = "Alf ET"
        
        use_case.execute(input=UpdateCastMember.Input(
            id=existing_castmember.id,
            name=new_name,
            type='DIRECTOR'
        ))
        mock_castmember_repository.get_by_id.assert_called_once_with(existing_castmember.id)
        mock_castmember_repository.update.assert_called_once()
