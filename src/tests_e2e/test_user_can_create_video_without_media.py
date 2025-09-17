import datetime
import dotenv
import jwt
import os
import pytest

from rest_framework.test import APIClient


dotenv.load_dotenv()

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
class TestCreateVideoWithoutMedia:
    def test_user_can_create_vide_without_media(self, auth_api_client) -> None:
        
        
        # Creates a new video
        create_response = auth_api_client.post(
            "/api/videos/", 
            {
                "title": "title",
                "description": "description",
                "launch_year": 2019,
                "opened": True,
                "rating": "L",
                "duration": 1,
                "categories": [
                    
                ],
                "genres": [
                    
                ],
                "cast_members": [
                    
                ]
            },
            )
        
        assert create_response.status_code == 201
        created_video_id = create_response.data["id"]
        assert created_video_id
        
        # Creates a new video with invalid genre
        create_response = auth_api_client.post(
            "/api/videos/", 
            {
                "title": "title",
                "description": "description",
                "launch_year": 2019,
                "opened": True,
                "rating": "L",
                "duration": 1,
                "categories": [
                    
                ],
                "genres": [
                    "invalid"
                    
                ],
                "cast_members": [
                    
                ]
            },
            )
        
        assert create_response.status_code == 400
        
        