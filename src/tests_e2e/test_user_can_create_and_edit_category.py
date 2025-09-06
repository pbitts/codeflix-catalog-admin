import pytest

from rest_framework.test import APIClient

@pytest.mark.django_db
class TestCreateAndEditCategory:
    def test_user_can_Create_and_edit_category(self) -> None:
        api_client = APIClient()
        
        # Verifies empty list
        list_response = api_client.get("/api/categories/")
        assert list_response.data == {"data": [], "meta": {
                                                    "per_page": 2, 
                                                    "total":0, 
                                                    "current_page":1}}
        
        # Creates a new category
        create_response = api_client.post(
            "/api/categories/", 
            {
                "name": "Movie",
                "description": "Category for movies"
                },
            )
        assert create_response.status_code == 201
        created_category_id = create_response.data["id"]
        
        # Verifies created categoru is listed
        list_response = api_client.get("/api/categories/")
        assert list_response.status_code == 200
        assert list_response.data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Movie",
                    "description": "Category for movies",
                    "is_active": True,
                }
            ],
            "meta": {
                                                    "per_page": 2, 
                                                    "total":1, 
                                                    "current_page":1}
        }
        
        # Updates the created category
        update_response = api_client.put(
            f"/api/categories/{created_category_id}/", 
            {
                "name": "Film",
                "description": "Category for films",
                "is_active": False,
            },
        )
        assert update_response.status_code == 204
        assert update_response.data is None
        
        # Verifies updated category is listed
        list_response = api_client.get("/api/categories/")
        assert list_response.data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Film",
                    "description": "Category for films",
                    "is_active": False,
                }
            ],
            "meta": {
                    "per_page": 2, 
                    "total":1, 
                    "current_page":1}
        }
    

@pytest.mark.django_db
class TestCreateAndDeleteCategory:
    def test_user_can_create_and_delete_category(self) -> None:
        api_client = APIClient()
        
        # Verifies empty list
        list_response = api_client.get("/api/categories/")
        assert list_response.data == {"data": [], "meta": {
                                                    "per_page": 2, 
                                                    "total":0, 
                                                    "current_page":1}}
        
        # Creates a new category
        create_response = api_client.post(
            "/api/categories/", 
            {
                "name": "Movie",
                "description": "Category for movies"
                },
            )
        assert create_response.status_code == 201
        created_category_id = create_response.data["id"]
        
        # Verifies created categoru is listed
        list_response = api_client.get("/api/categories/")
        assert list_response.status_code == 200
        assert list_response.data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Movie",
                    "description": "Category for movies",
                    "is_active": True,
                }
            ],
            "meta": {
                    "per_page": 2, 
                    "total":1, 
                    "current_page":1}
        }
        
        # Deletes the created category
        delete_response = api_client.delete(f"/api/categories/{created_category_id}/")
        assert delete_response.status_code == 204
        assert delete_response.data is None
        
        # Verifies empty list again
        list_response = api_client.get("/api/categories/")
        assert list_response.data == {"data": [], "meta": {
                                                    "per_page": 2, 
                                                    "total":0, 
                                                    "current_page":1}}
        