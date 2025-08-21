

import uuid
from src.core.category.application.use_cases.delete_category import DeleteCategory, DeleteCategoryRequest
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestDeleteCategory:
    def test_delete_category_from_repository(self):
        category_movie = Category(
            id=uuid.uuid4(),
            name="Movie",
            description="some description",
        )

        category_series= Category(
            id=uuid.uuid4(),
            name="Series",
            description="some description 2",
        )

        repository = InMemoryCategoryRepository(
            categories=[category_movie, category_series]
        ) # SQLAlchemy / DjangoORMRepository can be used here

        use_case = DeleteCategory(repository=repository)
        request = DeleteCategoryRequest(
            id=category_movie.id
        )
        
        assert repository.get_by_id(category_movie.id) is not None
        response = use_case.execute(request)

        assert repository.get_by_id(category_movie.id) is None
        assert response is None

