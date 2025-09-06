import pytest

from rest_framework.test import APIClient

@pytest.mark.django_db
class TestCreateAndEditCastMember:
    def test_user_can_Create_and_edit_category(self) -> None:
        api_client = APIClient()
        
        # Verifies empty list
        list_response = api_client.get("/api/cast_members/")
        assert list_response.data == {"data": [], "meta": {
                                                    "per_page": 2, 
                                                    "total":0, 
                                                    "current_page":1}}
        
        # Creates a new castmember
        create_response = api_client.post(
            "/api/cast_members/", 
            {
                "name": "Monica",
                "type": "DIRECTOR"
                },
            )
        assert create_response.status_code == 201
        created_castmember_id = create_response.data["id"]
        
        # Verifies created category is listed
        list_response = api_client.get("/api/cast_members/")
        assert list_response.status_code == 200
        assert list_response.data == {
            "data": [
                {
                    "id": created_castmember_id,
                    "name": "Monica",
                    "type": "DIRECTOR"
                }
            ],
            "meta": {
                    "per_page": 2, 
                    "total":1, 
                    "current_page":1}
        }
        
        # Updates the created castmember
        update_response = api_client.put(
            f"/api/cast_members/{created_castmember_id}/", 
            {
                "name": "Monica Updated",
                "type": 'ACTOR'
            },
        )
        assert update_response.status_code == 204
        assert update_response.data is None
        
        # Verifies updated category is listed
        list_response = api_client.get("/api/cast_members/")
        assert list_response.data == {
            "data": [
                {
                    "id": created_castmember_id,
                "name": "Monica Updated",
                "type": 'ACTOR'
                }
            ],
            "meta": {
                    "per_page": 2, 
                    "total":1, 
                    "current_page":1}
        }
    

@pytest.mark.django_db
class TestCreateAndDeleteCastMember:
    def test_user_can_create_and_delete_castmember(self) -> None:
        api_client = APIClient()
        
        # Verifies empty list
        list_response = api_client.get("/api/cast_members/")
        assert list_response.data == {"data": [], "meta": {
                                                    "per_page": 2, 
                                                    "total":0, 
                                                    "current_page":1}}
        
        # Creates a new castmember
        create_response = api_client.post(
            "/api/cast_members/", 
            {
                "name": "Magali",
                "type": "ACTOR"
                },
            )
        assert create_response.status_code == 201
        created_castmember_id = create_response.data["id"]
        
        # Verifies created castmember is listed
        list_response = api_client.get("/api/cast_members/")
        assert list_response.status_code == 200
        assert list_response.data == {
            "data": [
                {
                    "id": created_castmember_id,
                    "name": "Magali",
                "type": "ACTOR"
                }
            ],
            "meta": {
                        "per_page": 2, 
                        "total":1, 
                        "current_page":1}
        }
        
        # Deletes the created castmember
        delete_response = api_client.delete(f"/api/cast_members/{created_castmember_id}/")
        assert delete_response.status_code == 204
        assert delete_response.data is None
        
        # Verifies empty list again
        list_response = api_client.get("/api/cast_members/")
        assert list_response.data == {"data": [], "meta": {
                                                    "per_page": 2, 
                                                    "total":0, 
                                                    "current_page":1}}
        