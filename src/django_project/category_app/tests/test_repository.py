import pytest

from django_project.category_app.models import Category
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.category_app.models import Category as CategoryModel

@pytest.mark.django_db
class TestSave:
    def test_save_category_in_database(self):
        category = Category(
            name="Movie",
            description="some description"
            )
        repository = DjangoORMCategoryRepository()
        
        assert CategoryModel.objects.count() == 0
        repository.save(category)
        assert CategoryModel.objects.count() == 1
        
        category_db = CategoryModel.objects.get()
        assert category_db.id == category.id
        assert category_db.name == category.name
        assert category_db.description == category.description
        assert category_db.is_active == category.is_active

@pytest.mark.django_db
class TestGetByID:
    def test_category_by_id_in_database(self):
        category = Category(
            name="Movie",
            description="some description"
            )
        repository = DjangoORMCategoryRepository()
        repository.save(category)
        
        category_db = repository.get_by_id(category.id)
        assert category_db is not None
        assert category_db.id == category.id
        assert category_db.name == category.name
        assert category_db.description == category.description
        assert category_db.is_active == category.is_active

@pytest.mark.django_db
class TestDelete:
    def test_delete_category_in_database(self):
        category = Category(
            name="Movie",
            description="some description"
            )
        repository = DjangoORMCategoryRepository()
        repository.save(category)
        assert CategoryModel.objects.count() == 1
        
        repository.delete(category.id)
        assert CategoryModel.objects.count() == 0
        assert repository.get_by_id(category.id) is None

@pytest.mark.django_db
class TestList:
    def test_list_categories_in_database(self):
        category1 = Category(
            name="Movie",
            description="some description"
            )
        category2 = Category(
            name="Documentary",
            description="some description"
            )
        repository = DjangoORMCategoryRepository()
        repository.save(category1)
        repository.save(category2)
        
        categories = repository.list()
        assert len(categories) == 2
        assert categories[0].id == category1.id
        assert categories[1].id == category2.id
        assert categories[0].name == category1.name
        assert categories[1].name == category2.name
        assert categories[0].description == category1.description
        assert categories[1].description == category2.description
        assert categories[0].is_active == category1.is_active
        assert categories[1].is_active == category2.is_active
        
@pytest.mark.django_db
class TestUpdate:
    def test_update_category_in_database(self):
        category = Category(
            name="Movie",
            description="some description"
            )
        repository = DjangoORMCategoryRepository()
        repository.save(category)
        
        category.name = "Documentary"
        category.description = "other description"
        category.is_active = False
        repository.update(category)
        
        category_db = repository.get_by_id(category.id)
        assert category_db is not None
        assert category_db.id == category.id
        assert category_db.name == "Documentary"
        assert category_db.description == "other description"
        assert category_db.is_active is False
        
        
        