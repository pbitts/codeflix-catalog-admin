import uuid

import pytest

from src.core.castmember.application.exceptions import CastMemberNotFound
from src.core.castmember.application.use_cases.delete_castmember import DeleteCastMember
from src.core.castmember.domain.castmember import CastMember
from src.core.castmember.infra.in_memory_castmember_repository import InMemoryCastMemberRepository


class TestDeleteCastMember:
    def test_delete_castmember(self):
  
        castmember_repository = InMemoryCastMemberRepository()
        
        actor = CastMember(
            name="Alvin",
            type='ACTOR'
        )
        director = CastMember(
            name="Ravier",
            type='DIRECTOR'
        )
        castmember_repository.save(actor)
        castmember_repository.save(director)
        
        use_case = DeleteCastMember(
            repository=castmember_repository
        )
        
        output = use_case.execute(input=DeleteCastMember.Input(id=actor.id))
        assert output is None
        assert castmember_repository.list() == [director]
        
    def test_delete_castmember_not_found(self):
        castmember_repository = InMemoryCastMemberRepository()
        use_case = DeleteCastMember(
            repository=castmember_repository
        )
        
        with pytest.raises(CastMemberNotFound):
            use_case.execute(input=DeleteCastMember.Input(id=uuid.uuid4()))