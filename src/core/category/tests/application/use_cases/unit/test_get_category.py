from unittest.mock import create_autospec

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.domain.category import Category
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse


class TestGetCategory:
    def test_get_category_by_id(self):
        category = Category(
            name="Movie",
            description="some description",
            is_active=True
            )
        
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category
        use_case = GetCategory(repository=mock_repository)

        request = GetCategoryRequest(
            id=category.id
        )
        response = use_case.execute(request)

        assert response == GetCategoryResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active
        )
        mock_repository.get_by_id.assert_called_once_with(category.id)
        