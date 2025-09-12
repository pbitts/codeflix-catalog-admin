import uuid
import pytest

from src.core.castmember.domain.castmember import CastMember
from src.django_project.castmember_app.repository import DjangoORMCastMemberRepository
from src.django_project.castmember_app.models import CastMember as CastMemberModel


@pytest.mark.django_db
class TestSave:
    def test_save_castmember_in_db(self):
        repository = DjangoORMCastMemberRepository()
        castmember = CastMember(name="Alison", type='ACTOR')
        
        CastMemberModel.objects.count() == 0
        repository.save(castmember)
        
        assert CastMemberModel.objects.count() == 1
        castmember_model = CastMemberModel.objects.get(id=castmember.id)
        assert castmember_model.id == castmember.id
        assert castmember_model.name == "Alison"
        assert castmember_model.type == 'ACTOR'


@pytest.mark.django_db
class TestList:
    def test_list_castmember(self):
        repository = DjangoORMCastMemberRepository()
        castmember1 = CastMember(name="Han", type='ACTOR')
        castmember2 = CastMember(name="Rogerio", type='DIRECTOR')
        
        repository.save(castmember1)
        repository.save(castmember2)
        
        cast_members = repository.list()
        
        assert len(cast_members) == 2
        assert cast_members[0].id == castmember1.id
        assert cast_members[0].name == "Han"
        assert cast_members[0].type == 'ACTOR'
        
        assert cast_members[1].id == castmember2.id
        assert cast_members[1].name == "Rogerio"
        assert cast_members[1].type == 'DIRECTOR'
        
        
@pytest.mark.django_db
class TestGetById:
    def test_get_castmember_by_id(self):
        repository = DjangoORMCastMemberRepository()
        castmember = CastMember(name="Pablo", type='ACTOR')
        
        repository.save(castmember)
        
        found_castmember = repository.get_by_id(castmember.id)
        
        assert found_castmember is not None
        assert found_castmember.id == castmember.id
        assert found_castmember.name == "Pablo"
        assert found_castmember.type == 'ACTOR'
    
    def test_get_castmember_by_id_not_found(self):
        repository = DjangoORMCastMemberRepository()
        
        found_castmember = repository.get_by_id(uuid.uuid4())
        
        assert found_castmember is None
        

@pytest.mark.django_db
class TestUpdate:
    def test_update_castmember(self):
        repository = DjangoORMCastMemberRepository()
        
        castmember = CastMember(name="Helbert", type='DIRECTOR')
        repository.save(castmember)
        
        # Update genre details
        castmember.name = "Helbert L."
        castmember.type = 'ACTOR'
        
        repository.update(castmember)
        
        updated_castmember_model = CastMemberModel.objects.get(id=castmember.id)
        
        assert updated_castmember_model.name == "Helbert L."
        assert updated_castmember_model.type == 'ACTOR'
    
    def test_update_castmember_not_found(self):
        repository = DjangoORMCastMemberRepository()
        
        castmember = CastMember(name="Non-existent", type='ACTOR')
        
        result = repository.update(castmember)
        
        assert result is None
        
@pytest.mark.django_db
class TestDelete:
    def test_delete_castmember(self):
        repository = DjangoORMCastMemberRepository()
        castmember = CastMember(name="Juliana", type='DIRECTOR')
        
        repository.save(castmember)
        
        assert CastMemberModel.objects.count() == 1
        
        repository.delete(castmember.id)
        
        assert CastMemberModel.objects.count() == 0
    
    def test_delete_castmember_not_found(self):
        repository = DjangoORMCastMemberRepository()
        repository = DjangoORMCastMemberRepository()
        castmember = CastMember(name="Keyla", type='ACTOR')
        
        repository.save(castmember)
        assert CastMemberModel.objects.count() == 1
        
        repository.delete(uuid.uuid4())
        
        assert CastMemberModel.objects.count() == 1
        assert CastMemberModel.objects.get(id=castmember.id) is not None