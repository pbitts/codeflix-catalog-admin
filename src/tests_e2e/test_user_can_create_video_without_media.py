import pytest

from rest_framework.test import APIClient

@pytest.mark.django_db
class TestCreateVideoWithoutMedia:
    def test_user_can_create_vide_without_media(self) -> None:
        api_client = APIClient()
        
        # Creates a new video
        create_response = api_client.post(
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
        create_response = api_client.post(
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
        
        