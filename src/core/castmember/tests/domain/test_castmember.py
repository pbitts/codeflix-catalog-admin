import pytest
from uuid import UUID
import uuid

from src.core.castmember.domain.castmember import CastMember

class TestCastMember:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 2 required positional arguments: 'name' and 'type'"):
            CastMember()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name cannot be longer than 255"):
            CastMember("a" * 256, type='ACTOR')
    
    def test_type_must_be_either_actor_or_director(self):
        with pytest.raises(ValueError, match="Type must be either 'ACTOR' or 'DIRECTOR'"):
            CastMember(name='John', type='INVALID')
        

    def test_cast_is_created_with_valid_values(self):
        cat_id = uuid.uuid4()
        castmember = CastMember(
            id=cat_id,
            name="Higor",
            type="DIRECTOR"
        )
        
        assert castmember.name == "Higor"
        assert castmember.type == "DIRECTOR"
        assert castmember.id == cat_id

    def test_cannot_create_genre_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            CastMember(name="", type="DIRECTOR")

        
class TestEquality:
    def test_when_castmember_have_same_id_they_are_equal(self):
        common_id = uuid.uuid4()
        castmember1 = CastMember(id=common_id, name='John', type='ACTOR')
        castmember2 = CastMember(id=common_id, name='Rick', type='ACTOR')
        assert castmember1 == castmember2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        common_id = uuid.uuid4()
        castmember = CastMember(id=common_id, name='Cameron',type='ACTOR')
        dummy = Dummy()
        dummy.id = common_id

        assert castmember != dummy

class TestChangeName:
    def test_change_name(self):
        castmember = CastMember(name='Cam', type='ACTOR')
        castmember.change_name('Roger')
        assert castmember.name == 'Roger'

    def test_change_name_to_empty_raises_error(self):
        castmember = CastMember(name='Cam', type='ACTOR')
        with pytest.raises(ValueError, match="name cannot be empty"):
            castmember.change_name('')

class TestUpdateType:
    def test_update_type(self):
        castmember = CastMember(name='Higor', type='ACTOR')
        assert castmember.type == 'ACTOR'
        castmember.update_type('DIRECTOR')
        assert castmember.type == 'DIRECTOR'
    
    def test_update_with_invalid_type_raise_error(self):
        castmember = CastMember(name='Higor', type='ACTOR')
        assert castmember.type == 'ACTOR'
        with pytest.raises(ValueError, match="Type must be either 'ACTOR' or 'DIRECTOR'"):
            castmember.update_type('INVALID')
        