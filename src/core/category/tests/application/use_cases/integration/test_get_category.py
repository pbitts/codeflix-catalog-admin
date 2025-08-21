

import uuid

import pytest
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound

class TestGetCategory:
    def test_get_category_by_id(self):
        category_movie = Category(
            name="Movie",
            description="some description",
        )

        category_series= Category(
            name="Series",
            description="some description 2",
        )

        repository = InMemoryCategoryRepository(
            categories=[category_movie, category_series]
        ) # SQLAlchemy / DjangoORMRepository can be used here

        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(
            id=category_movie.id
        )
        response = use_case.execute(request)

        assert response == GetCategoryResponse(
            id=category_movie.id,
            name="Movie",
            description="some description",
            is_active=True
        )
    
    def test_get_category_not_found_then_raise_exception(self):
        category_movie = Category(
            name="Movie",
            description="some description",
        )

        category_series= Category(
            name="Series",
            description="some description 2",
        )

        repository = InMemoryCategoryRepository(
            categories=[category_movie, category_series]
        ) # SQLAlchemy / DjangoORMRepository can be used here

        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(
            id=uuid.uuid4()
        )
        with pytest.raises(CategoryNotFound) as exc_info: 
            use_case.execute(request)
