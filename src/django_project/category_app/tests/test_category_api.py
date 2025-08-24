import uuid
import pytest
from rest_framework.test import APIClient
from rest_framework.status import (
    HTTP_200_OK, 
    HTTP_400_BAD_REQUEST, 
    HTTP_404_NOT_FOUND)

from src.core.category.domain.category import Category
from django_project.category_app.repository import DjangoORMCategoryRepository


@pytest.fixture
def category_movie():
    return Category(
        name="Movie",
        description="Movie Description"
    )
    
@pytest.fixture
def category_documentary():
    return Category(
        name="Documentary",
        description="Documentary Description"
    )
    
@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()
    
@pytest.mark.django_db
class TestCategoryAPI:
    def test_list_categories(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository
        ) -> None:
        
        
        category_repository.save(category_movie)
        category_repository.save(category_documentary)
        
        response = APIClient().get('/api/categories/')
        
        expected_data = [
            {
                "id": str(category_movie.id),
                "name": category_movie.name,
                "description": category_movie.description,
                "is_active": category_movie.is_active
            },
            {
                "id": str(category_documentary.id),
                "name": category_documentary.name,
                "description": category_documentary.description,
                "is_active": category_documentary.is_active
            }
        ]
        
        assert response.status_code == HTTP_200_OK
        assert response.data == expected_data
        
@pytest.mark.django_db        
class TestRetrieveCategoryAPI:
    def test_retrieve_category_invalid_id_return_400(self) -> None:
        
        response = APIClient().get('/api/categories/123123123/')
        
        assert response.status_code == HTTP_400_BAD_REQUEST
        
    def test_retrieve_category_when_exists(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository
        ) -> None:
        
        category_repository.save(category_movie)
        category_repository.save(category_documentary)
        
        response = APIClient().get(f'/api/categories/{category_movie.id}/')
        
        expected_data = {
            "id": str(category_movie.id),
            "name": category_movie.name,
            "description": category_movie.description,
            "is_active": category_movie.is_active
        }
        
        assert response.status_code == HTTP_200_OK
        assert response.data == expected_data
    
    def test_retrieve_category_not_found_return_404(self) -> None:
        
        response = APIClient().get(f'/api/categories/{uuid.uuid4()}/')
        
        assert response.status_code == HTTP_404_NOT_FOUND
