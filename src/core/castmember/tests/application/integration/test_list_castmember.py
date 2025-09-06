

from src.core._shared.meta import ListOutputMeta
from src.core.castmember.application.use_cases.list_castmember import ListCastMember, CastMemberOutput
from src.core.castmember.domain.castmember import CastMember
from src.core.castmember.infra.in_memory_castmember_repository import InMemoryCastMemberRepository


class TestListCastMember:
    def test_list_castmember(
        self,
    ):
        
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
        
        use_case = ListCastMember(
            repository=castmember_repository
        )
        
        output = use_case.execute(ListCastMember.Input())
        
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
    
    def test_list_empty_castmember_list(
        self,
    ):
        castmember_repository = InMemoryCastMemberRepository()
        use_case = ListCastMember(
            repository=castmember_repository
        )
        
        output = use_case.execute(ListCastMember.Input())
        
        assert len(output.data) == 0
        assert output == ListCastMember.Output(data=[], meta=ListOutputMeta(current_page=1,
                                                      per_page=2,
                                                      total=0))