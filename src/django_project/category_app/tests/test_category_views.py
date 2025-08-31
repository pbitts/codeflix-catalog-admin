import uuid
from uuid import UUID
import pytest
from rest_framework.test import APIClient
from rest_framework.status import (
    HTTP_200_OK, 
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST, 
    HTTP_404_NOT_FOUND
    )

from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository


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
class TesListCategoryAPI:
    def test_list_categories(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository
        ) -> None:
        
        
        category_repository.save(category_movie)
        category_repository.save(category_documentary)
        
        response = APIClient().get('/api/categories/')
        
        expected_data = {
            "data": [
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
        ],
        }
        
        assert response.status_code == HTTP_200_OK
        assert len(response.data["data"]) == 2
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
            'data': 
                {"id": str(category_movie.id),
                "name": category_movie.name,
                "description": category_movie.description,
                "is_active": category_movie.is_active}
        }
        
        assert response.status_code == HTTP_200_OK
        assert response.data == expected_data
    
    def test_retrieve_category_not_found_return_404(self) -> None:
        
        response = APIClient().get(f'/api/categories/{uuid.uuid4()}/')
        
        assert response.status_code == HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestCreateCategoryAPI:
    def test_when_payload_is_invalid_then_return_400(self) -> None:
        response = APIClient().post(
            '/api/categories/', 
            data={
                "name": "", 
                "description": "some description"
                }
        )
        
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."],
        }
    
    def test_when_payload_is_valid_then_create_category_and_return_201(
        self,
        category_repository: DjangoORMCategoryRepository
        ) -> None:
        
        response = APIClient().post(
            '/api/categories/', 
            data={
                "name": "Movie", 
                "description": "Movie description"
                }
        )
        
        assert response.status_code == HTTP_201_CREATED
        created_category_id = uuid.UUID(response.data["id"])
        
        saved_category = category_repository.get_by_id(created_category_id)
        
        assert saved_category == Category(
            id=created_category_id,
            name="Movie",
            description="Movie description",
        )
        
        assert category_repository.list() == [
            Category(
                id=uuid.UUID(response.data["id"]),
                name="Movie",
                description="Movie description",
            )
        ]


@pytest.mark.django_db
class TestUpdateCategoryAPI:
    def test_when_payload_is_invalid_then_return_400(
        self
        ) -> None:
        
        response = APIClient().put(
            f'/api/categories/112233/', 
            data={
                "name": "", 
                "description": "some description"
                # is_active is missing
                },
            format='json'
        )
        
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {
            "id": ["Must be a valid UUID."],
            "name": ["This field may not be blank."],
            "is_active": ["This field is required."]
        }
    
    def test_when_payload_is_valid_then_update_category_and_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        
        category_repository.save(category_movie)
        
        response = APIClient().put(
            f'/api/categories/{category_movie.id}/', 
            data={
                "name": "Updated Movie", 
                "description": "Updated Movie description",
                "is_active": False
                }
        )
        
        assert response.status_code == HTTP_204_NO_CONTENT
        
        updated_category = category_repository.get_by_id(category_movie.id)
        
        assert updated_category.name == "Updated Movie"
        assert updated_category.description == "Updated Movie description"
        assert updated_category.is_active is False
    
    def test_when_category_doesnot_exist_then_return_404(self):
        response = APIClient().put(
            f'/api/categories/{uuid.uuid4()}/', 
            data={
                "name": "Updated Movie", 
                "description": "Updated Movie description",
                "is_active": False
                }
        )
        
        assert response.status_code == HTTP_404_NOT_FOUND
        
@pytest.mark.django_db
class TestDeleteCategoryAPI:
    def test_delete_category_invalid_id_return_400(self) -> None:
        
        response = APIClient().delete('/api/categories/123123123/')
        
        assert response.status_code == HTTP_400_BAD_REQUEST
        
    def test_delete_category_when_exists(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository
        ) -> None:
        
        category_repository.save(category_movie)
        category_repository.save(category_documentary)
        
        response = APIClient().delete(f'/api/categories/{category_movie.id}/')
        
        assert response.status_code == HTTP_204_NO_CONTENT
        assert category_repository.list() == [category_documentary]
    
    def test_delete_category_not_found_return_404(self) -> None:
        
        response = APIClient().delete(f'/api/categories/{uuid.uuid4()}/')
        
        assert response.status_code == HTTP_404_NOT_FOUND
    

@pytest.mark.django_db
class TestPartialUpdateCategoryAPI:
    def test_update_name_invalid_id_return_400(self) -> None:
        
        response = APIClient().patch(
            '/api/categories/123123123/', 
            data={
                "name": "Updated Movie"
                }
        )
        
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {
            "id": ["Must be a valid UUID."],
        }
    
    def test_update_name_invalid_name_return_400(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository
        ) -> None:
        
        category_repository.save(category_movie)
        
        response = APIClient().patch(
            f'/api/categories/{category_movie.id}/', 
            data={
                "name": ""
                }
        )
        
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."],
        }
    
    def test_update_name_inavlid_size_return_400(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository
        ) -> None:
        
        category_repository.save(category_movie)
        
        response = APIClient().patch(
            f'/api/categories/{category_movie.id}/', 
            data={
                "name": "x" * 256
                }
        )
        
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["Ensure this field has no more than 255 characters."],
        }
    
    def test_update_name_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository
        ) -> None:
        
        category_repository.save(category_movie)
        
        response = APIClient().patch(
            f'/api/categories/{category_movie.id}/', 
            data={
                "name": "Updated Movie"
                }
        )
        
        assert response.status_code == HTTP_204_NO_CONTENT
        
        updated_category = category_repository.get_by_id(category_movie.id)
        
        assert updated_category.name == "Updated Movie"
        assert updated_category.description == category_movie.description
        assert updated_category.is_active is category_movie.is_active
    
    def test_update_description_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository
        ) -> None:
        
        category_repository.save(category_movie)
        
        response = APIClient().patch(
            f'/api/categories/{category_movie.id}/', 
            data={
                "description": "Updated Movie description"
                }
        )
        
        assert response.status_code == HTTP_204_NO_CONTENT
        
        updated_category = category_repository.get_by_id(category_movie.id)
        
        assert updated_category.name == category_movie.name
        assert updated_category.description == "Updated Movie description"
        assert updated_category.is_active is category_movie.is_active
    
    def test_update_is_active_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository
        ) -> None:
        
        category_repository.save(category_movie)
        
        response = APIClient().patch(
            f'/api/categories/{category_movie.id}/', 
            data={
                "is_active": False
                }
        )
        
        assert response.status_code == HTTP_204_NO_CONTENT
        
        updated_category = category_repository.get_by_id(category_movie.id)
        
        assert updated_category.name == category_movie.name
        assert updated_category.description == category_movie.description
        assert updated_category.is_active is False