

from core.castmember.application.use_cases.update_castmember import UpdateCastMember
from core.castmember.domain.castmember import CastMember
from core.castmember.infra.in_memory_castmember_repository import InMemoryCastMemberRepository


class TestUpdateCastMember:
    def test_update_castmember_with_valid_attributes(
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
        
        saved_actor = castmember_repository.get_by_id(actor.id)
        saved_director = castmember_repository.get_by_id(director.id)
        assert saved_actor == actor
        assert saved_director == director
        assert saved_actor.type == 'ACTOR'
        assert saved_director.type == 'DIRECTOR' 
        
        use_case = UpdateCastMember(
            repository=castmember_repository
        )
        
        use_case.execute(UpdateCastMember.Input(id=actor.id,
                                            name="Alvin 2",
                                            type='DIRECTOR'))
        
        use_case.execute(UpdateCastMember.Input(id=director.id,
                                            name="Ravier 2",
                                            type='ACTOR')) 
        
        output_actor_updated = castmember_repository.get_by_id(actor.id)
        output_director_updated = castmember_repository.get_by_id(director.id)
        
        assert output_actor_updated.name == "Alvin 2"
        assert output_actor_updated.type == 'DIRECTOR'
        
        assert output_director_updated.name == "Ravier 2" 
        assert output_director_updated.type == 'ACTOR'