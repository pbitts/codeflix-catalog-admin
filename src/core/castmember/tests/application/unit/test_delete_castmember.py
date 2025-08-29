from unittest.mock import create_autospec
import uuid

import pytest

from src.core.castmember.application.exceptions import CastMemberNotFound
from src.core.castmember.application.use_cases.delete_castmember import DeleteCastMember
from src.core.castmember.domain.castmember import CastMember
from src.core.castmember.domain.castmember_repository import CastMemberRepository


@pytest.fixture
def mock_castmember_repository():
    return create_autospec(CastMemberRepository)

class TestDeleteCastMember:
    def test_delete_castmember(self, mock_castmember_repository):
        castmember = CastMember(name='Rie', type='ACTOR')
        mock_castmember_repository.get_by_id.return_value = castmember
        use_case = DeleteCastMember(mock_castmember_repository)
        use_case.execute(DeleteCastMember.Input(id=castmember.id))
        mock_castmember_repository.get_by_id.assert_called_once_with(castmember.id)
        mock_castmember_repository.delete.assert_called_once_with(castmember.id)

    def test_delete_castmember_not_found(self, mock_castmember_repository):
        mock_castmember_repository.get_by_id.return_value = None
        use_case = DeleteCastMember(mock_castmember_repository)
        
        fake_id = uuid.uuid4()
        with pytest.raises(CastMemberNotFound, match=f"CastMember with id {str(fake_id)} not found"):
            use_case.execute(DeleteCastMember.Input(id=fake_id))
            
        mock_castmember_repository.get_by_id.assert_called_once()
        mock_castmember_repository.delete.assert_not_called()
        