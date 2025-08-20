from uuid import UUID

from src.core.category.application.use_cases.create_category import CreateCategory, CreateCategoryRequest
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        repository = InMemoryCategoryRepository() # SQLAlchemy / DjangoORMRepository can be used here
        use_case = CreateCategory(repository=repository)
        request = CreateCategoryRequest(
            name="Movie",
            description="some description",
            is_active=True  # default
        )
        response = use_case.execute(request)

        assert response is not None
        assert isinstance(response.id, UUID)
        assert len(repository.categories) == 1
        assert repository.categories[0].id == response.id
        assert repository.categories[0].name == "Movie"
        assert repository.categories[0].description == "some description"
        assert repository.categories[0].is_active is True
