from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestSave:
    def test_can_save_category(self):
        repository = InMemoryCategoryRepository()
        category = Category(name="Movie", description="some description")
        repository.save(category)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category

class TestGetById:
    def test_get_category_by_id(self):
        repository = InMemoryCategoryRepository()
        category = Category(name="Movie", description="some description")
        repository.save(category)

        response = repository.get_by_id(category.id)
        assert response is not None
        assert response.id == category.id

class TestDeleteById:
    def test_delete_category_by_id(self):
        repository = InMemoryCategoryRepository()
        category = Category(name="Movie", description="some description")
        repository.save(category)

        response = repository.get_by_id(category.id)
        assert response is not None
        assert response.id == category.id
        
        response = repository.delete(category.id)
        assert response is None