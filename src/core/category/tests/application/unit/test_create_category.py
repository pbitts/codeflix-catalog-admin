from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.create_category import CreateCategory, CreateCategoryRequest, CreateCategoryResponse
from src.core.category.application.exceptions import InvalidCategoryData


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        mock_repository = MagicMock(CategoryRepository)
        use_case = CreateCategory(repository=mock_repository)
        request = CreateCategoryRequest(
            name="Movie",
            description="some description",
            is_active=True  # default
        )
        response = use_case.execute(request)

        assert isinstance(response.id, UUID)
        assert isinstance(response, CreateCategoryResponse)
        assert mock_repository.save.called is True

    def test_create_category_with_invalid_data(self):
        use_case = CreateCategory(repository=MagicMock(CategoryRepository))
        with pytest.raises(InvalidCategoryData) as exc_info:
            response = use_case.execute(CreateCategoryRequest(
                name="",  # Invalid name
            ))
        
        assert exc_info.type is InvalidCategoryData
        assert str(exc_info.value) == "name cannot be empty"
        