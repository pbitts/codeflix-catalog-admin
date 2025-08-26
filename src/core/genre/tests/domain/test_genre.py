import pytest
from uuid import UUID
import uuid

from src.core.genre.domain.genre import Genre

class TestGenre:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            Genre()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name cannot be longer than 255"):
            Genre("a" * 256)

    def test_created_genre_with_default_values(self):
        genre = Genre(name="SciFi")
        assert genre.name == "SciFi"
        assert genre.is_active is True
        assert genre.id is not None
        assert isinstance(genre.id, UUID)
        assert genre.categories == set()

    def test_genre_is_created_with_provided_values(self):
        cat_id = uuid.uuid4()
        genre = Genre(
            id=cat_id,
            name="SciFi",
            is_active=False,
            categories={uuid.uuid4(), uuid.uuid4()}
        )
        
        assert genre.name == "SciFi"
        assert genre.is_active is False
        assert genre.id == cat_id
        assert isinstance(genre.id, UUID)
        assert len(genre.categories) == 2


        
    
    def test_cannot_create_genre_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Genre(name="")

class TestActivate:
    def test_activate_genre(self):
        genre = Genre(name='Romance')

        genre.activate()

        assert genre.is_active is True
    
    def test_activate_inactive_genre(self):
        genre = Genre(name='Comedy')

        genre.activate()

        assert genre.is_active is True
    
class TestDeactivate:
        def test_deactivate_genre(self):
            genre = Genre(name='Comedy')

            genre.deactivate()

            assert genre.is_active is False

        def test_deactivate_active_genre(self):
            genre = Genre(name='Comedy')

            genre.deactivate()

            assert genre.is_active is False
        
class TestEquality:
    def test_when_genres_have_same_id_they_are_equal(self):
        common_id = uuid.uuid4()
        genre_1 = Genre(name='Movie', id=common_id)
        genre_2 = Genre(name='Movie', id=common_id)
        assert genre_1 == genre_2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        common_id = uuid.uuid4()
        genre = Genre(name='Comedy', id=common_id)
        dummy = Dummy()
        dummy.id = common_id

        assert genre != dummy

class TestChangeName:
    def test_change_name(self):
        genre = Genre(name='Comedy')
        genre.change_name('Drama')
        assert genre.name == 'Drama'

    def test_change_name_to_empty_raises_error(self):
        genre = Genre(name='Drama')
        with pytest.raises(ValueError, match="name cannot be empty"):
            genre.change_name('')

class TestAddCategory:
    def test_add_category(self):
        genre = Genre(name='Horror')
        category_id = uuid.uuid4()
        assert category_id not in genre.categories
        genre.add_category(category_id)
        assert category_id in genre.categories
        assert len(genre.categories) == 1
    
    def test_can_add_multiple_categories(self):
        genre = Genre(name='Horror')
        category_id1 = uuid.uuid4()
        category_id2 = uuid.uuid4()
        genre.add_category(category_id1)
        genre.add_category(category_id2)
        assert category_id1 in genre.categories
        assert category_id2 in genre.categories
        assert len(genre.categories) == 2
        
class TestRemoveCategory:
    def test_remove_category(self):
        category_id = uuid.uuid4()
        genre = Genre(name='Horror', categories={category_id})
        assert category_id in genre.categories
        genre.remove_category(category_id)
        assert category_id not in genre.categories
        assert len(genre.categories) == 0

    def test_remove_nonexistent_category_raises_error(self):
        genre = Genre(name='Horror')
        category_id = uuid.uuid4()
        with pytest.raises(KeyError):
            genre.remove_category(category_id)