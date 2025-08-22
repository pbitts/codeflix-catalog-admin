from unittest.mock import create_autospec
import uuid

import pytest

from src.core.category.application.use_cases.exceptions import CategoryNotFound, InvalidCategoryData
from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.domain.category import Category


class TestUpdateCategory:
    def test_update_category_name(self):
        category = Category(id=uuid.uuid4(), name="Movie", description="some description")
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category
        
        use_case = UpdateCategory(repository=mock_repository)
        use_case.execute(UpdateCategoryRequest(id=category.id, name="Updated Movie"))
        
        assert category.name == "Updated Movie"
        assert category.description == "some description"
        mock_repository.update.assert_called_once_with(category)
    
    def test_update_category_description(self):
        category = Category(id=uuid.uuid4(), name="Movie", description="some description")
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category
        
        use_case = UpdateCategory(mock_repository)
        use_case.execute(UpdateCategoryRequest(id=category.id, description="Updated description"))
        
        assert category.name == "Movie"
        assert category.description == "Updated description"
        mock_repository.update.assert_called_once_with(category)
    
    def test_can_deactivate_category(self):
        category = Category(id=uuid.uuid4(), name="Movie", description="some description", is_active=True)
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category
        
        use_case = UpdateCategory(mock_repository)
        use_case.execute(UpdateCategoryRequest(id=category.id, is_active=False))
        
        assert category.is_active is False
        mock_repository.update.assert_called_once_with(category)
    
    def test_can_activate_category(self):
        category = Category(id=uuid.uuid4(), name="Movie", description="some description", is_active=False)
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category
        
        use_case = UpdateCategory(mock_repository)
        use_case.execute(UpdateCategoryRequest(id=category.id, is_active=True))
        
        assert category.is_active is True
        mock_repository.update.assert_called_once_with(category)
    
    def test_update_fake_category_then_raises_exception(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None
        
        use_case = UpdateCategory(mock_repository)
        
        with pytest.raises(CategoryNotFound):
            use_case.execute(UpdateCategoryRequest(id=uuid.uuid4(), name="Fake Category"))
        
        mock_repository.update.assert_not_called()
        mock_repository.get_by_id.assert_called_once()
    
    def test_update_category_invalid_name(self):
        category = Category(id=uuid.uuid4(), name="Movie", description="some description")
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category
        
        use_case = UpdateCategory(mock_repository)
        
        with pytest.raises(InvalidCategoryData):
            use_case.execute(UpdateCategoryRequest(id=category.id, name="a"*256))
        
        mock_repository.update.assert_not_called()
        mock_repository.get_by_id.assert_called_once_with(category.id)