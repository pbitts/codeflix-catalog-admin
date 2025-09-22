import datetime
import dotenv
import jwt
import os
import pytest

from rest_framework.test import APIClient


dotenv.load_dotenv(dotenv_path=".env.example")

@pytest.fixture
def admin_jwt_token():
    raw_private_key = os.getenv("AUTH_TEST_PRIVATE_KEY")
    private_key = f"-----BEGIN PRIVATE KEY-----\n{raw_private_key}\n-----END PRIVATE KEY-----"
    payload = {
        "aud": "account",
        "realm_access": {
            "roles": [
                "offline_access",
                "admin",
                "uma_authorization",
                "default-roles-codeflix"
            ]
        },
        
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1),
        "iat": datetime.datetime.now(datetime.UTC) ,
    }
    
    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token
    
@pytest.fixture
def auth_api_client(admin_jwt_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_jwt_token}")
    return client

@pytest.mark.django_db
class TestCreateAndEditCategory:
    def test_user_can_Create_and_edit_category(self, auth_api_client) -> None:
        
        
        # Verifies empty list
        list_response = auth_api_client.get("/api/categories/")
        assert list_response.data == {"data": [], "meta": {
                                                    "per_page": 2, 
                                                    "total":0, 
                                                    "current_page":1}}
        
        # Creates a new category
        create_response = auth_api_client.post(
            "/api/categories/", 
            {
                "name": "Movie",
                "description": "Category for movies"
                },
            )
        assert create_response.status_code == 201
        created_category_id = create_response.data["id"]
        
        # Verifies created categoru is listed
        list_response = auth_api_client.get("/api/categories/")
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
        update_response = auth_api_client.put(
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
        list_response = auth_api_client.get("/api/categories/")
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
    def test_user_can_create_and_delete_category(self, auth_api_client) -> None:
        
        
        # Verifies empty list
        list_response = auth_api_client.get("/api/categories/")
        assert list_response.data == {"data": [], "meta": {
                                                    "per_page": 2, 
                                                    "total":0, 
                                                    "current_page":1}}
        
        # Creates a new category
        create_response = auth_api_client.post(
            "/api/categories/", 
            {
                "name": "Movie",
                "description": "Category for movies"
                },
            )
        assert create_response.status_code == 201
        created_category_id = create_response.data["id"]
        
        # Verifies created categoru is listed
        list_response = auth_api_client.get("/api/categories/")
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
        delete_response = auth_api_client.delete(f"/api/categories/{created_category_id}/")
        assert delete_response.status_code == 204
        assert delete_response.data is None
        
        # Verifies empty list again
        list_response = auth_api_client.get("/api/categories/")
        assert list_response.data == {"data": [], "meta": {
                                                    "per_page": 2, 
                                                    "total":0, 
                                                    "current_page":1}}
        