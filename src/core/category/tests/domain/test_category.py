import pytest
from uuid import UUID
import uuid

from src.core.category.domain.category import Category

class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            Category()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name cannot be longer than 255"):
            Category("a" * 256)

    def test_category_must_be_created_with_id_as_uuid(self):
        category = Category("Movie")
        assert isinstance(category.id, UUID)

    def test_created_category_with_default_values(self):
        category = Category("Movie")
        assert category.name == "Movie"
        assert category.description == ""
        assert category.is_active is True

    def test_category_is_created_as_active_by_default(self):
        category = Category("Movie")
        assert category.is_active is True

    def test_category_is_created_with_provided_values(self):
        cat_id = uuid.uuid4()
        category = Category(
            id=cat_id,
            name="Movie",
            description="some description",
            is_active=False
        )
        assert category.id == cat_id
        assert category.name == "Movie"
        assert category.description == "some description"
        assert category.is_active is False

    def test_category_str_method(self):
        category = Category("Movie")
        assert str(category) == "Category(name=Movie - description= (is_active=True))"

    def test_category_repr_method(self):
        category = Category("Movie")
        assert repr(category) == "Category(name=Movie - description= (is_active=True))"
    
    def test_cannot_create_category_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Category(name="")
    
    def test_description_must_have_less_than_1024_chars(self):
        with pytest.raises(ValueError, match="description cannot be longer than 1024"):
            Category(name='Movie', description="a" * 1025)
    
    def test_cannot_create_category_with_empty_name_and_description_must_have_less_than_1024_chars(self):
        with pytest.raises(ValueError, match="^name cannot be empty, description cannot be longer than 1024$"):
            Category(name='', description="a" * 1025)

    class TestUpdateCategory:
        def test_update_category_with_name_and_description(self):
            category = Category("Movie", "some description", True)
            category.update_category("Movie 2", "some description 2")
            assert category.name == "Movie 2"
            assert category.description == "some description 2"

        def test_update_category_with_only_name(self):
            category = Category("Movie", "some description", True)
            category.update_category("Movie 2")
            assert category.name == "Movie 2"

        def test_update_category_with_only_description(self):
            category = Category("Movie", "some description", True)
            category.update_category(description="some description 2")
            assert category.description == "some description 2"
        
        def test_update_category_with_invalid_name(self):
            category = Category(name='Movie', description='some description')

            with pytest.raises(ValueError, match='name cannot be longer than 255'):
                category.update_category(name="a" *256, description="some description 2")

        class TestActivate:
            def test_activate_category(self):
                category = Category(name='Movie', description='some description')

                category.activate()

                assert category.is_active is True
            
            def test_activate_inactive_category(self):
                category = Category(name='Movie', description='some description', is_active=False)

                category.activate()

                assert category.is_active is True
        
    class TestDeactivate:
            def test_deactivate_category(self):
                category = Category(name='Movie', description='some description')

                category.deactivate()

                assert category.is_active is False

            def test_deactivate_active_category(self):
                category = Category(name='Movie', description='some description', is_active=True)

                category.deactivate()

                assert category.is_active is False
        
class TestEquality:
    def test_when_categories_have_same_id_they_are_equal(self):
        common_id = uuid.uuid4()
        category_1 = Category(name='Movie', id=common_id)
        category_2 = Category(name='Movie', id=common_id)
        assert category_1 == category_2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        common_id = uuid.uuid4()
        category = Category(name='Movie', id=common_id)
        dummy = Dummy()
        dummy.id = common_id

        assert category != dummy

    