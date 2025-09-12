from unittest.mock import create_autospec
import pytest

from src.core._shared.meta import ListOutputMeta
from core.castmember.application.use_cases.list_castmember import CastMemberOutput, ListCastMember
from core.castmember.domain.castmember import CastMember
from core.castmember.domain.castmember_repository import CastMemberRepository




@pytest.fixture
def mock_castmember_repository() -> CastMemberRepository:
    return create_autospec(CastMemberRepository)
    

class TestListCastMember:
    def test_when_no_cast_members_exist_then_return_empty_list(
        self,
        mock_castmember_repository: CastMemberRepository
    ):
        mock_castmember_repository.list.return_value = []
        
        use_case = ListCastMember(
            repository=mock_castmember_repository
        )
        
        output = use_case.execute(input=ListCastMember.Input())
        
        assert output == ListCastMember.Output(data=[], meta=ListOutputMeta(current_page=1,
                                                      per_page=2,
                                                      total=0))
        mock_castmember_repository.list.assert_called_once()
    
    def test_when_cast_members_exist_then_return_genre_list(
        self,
        mock_castmember_repository: CastMemberRepository,
    ):
        actor = CastMember(
            name="Albert",
            type="ACTOR"
        )
        director = CastMember(
            name="Julio",
            type="DIRECTOR"
        )
        mock_castmember_repository.list.return_value = [actor, director]
        
        use_case = ListCastMember(
            repository=mock_castmember_repository
        )
        
        output = use_case.execute(input=ListCastMember.Input())
        
        assert len(output.data) == 2
        assert output == ListCastMember.Output(
            data=[
                CastMemberOutput(
                    id=actor.id,
                    name=actor.name,
                    type=actor.type
                ),
                CastMemberOutput(
                   id=director.id,
                    name=director.name,
                    type=director.type
                )
            ],
            meta=ListOutputMeta(
                current_page=1,
                per_page=2,
                total=2
            )
        )
        mock_castmember_repository.list.assert_called_once()
    
            