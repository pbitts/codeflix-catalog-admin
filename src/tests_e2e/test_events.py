import pytest
import json
import pika

from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

from src.django_project.video_app.models import Video

@pytest.mark.django_db
class TestEvents:
    def test_events(self) -> None:
        api_client = APIClient()
        
        # Creates a new category
        create_category_response = api_client.post(
            "/api/categories/", 
            {
                "name": "Movie",
                "description": "Category for movies"
                },
            )
        assert create_category_response.status_code == 201
        category_id = create_category_response.data["id"]
        
        # Creates new castmember
        create_castmembers_response = api_client.post(
            "/api/cast_members/", 
            {
                "name": "Monica",
                "type": "DIRECTOR"
                },
            )
        assert create_castmembers_response.status_code == 201
        castmember_id = create_castmembers_response.data["id"]
        
        # Creates new genre
        create_genres_response = api_client.post(
            "/api/genres/", 
            {
                "name": "Romance",
                "is_active": "True",
                "categories": [category_id]
                },
            )
        assert create_genres_response.status_code == 201
        genre_id = create_genres_response.data["id"]
        
        # Creates Video without Media
        create_video_response = api_client.post(
            "/api/videos/", 
            {
                "title": "title",
                "description": "description",
                "launch_year": 2019,
                "opened": True,
                "rating": "L",
                "duration": 1,
                "categories": [
                    category_id
                ],
                "genres": [
                    genre_id
                ],
                "cast_members": [
                    castmember_id
                ]
            },
            )
        
        assert create_video_response.status_code == 201
        video_id = create_video_response.data["id"]
        
        # Upload Media
        video_file = SimpleUploadedFile("sample.mp4", b"fake-video-content", content_type="video/mp4")
        upload_media_response = api_client.patch(
                f"/api/videos/{video_id}/",
                {"video_file": video_file},
                format="multipart"
                )
        assert upload_media_response.status_code == 200
        
        # Sends message to queue vide.converted
        
        QUEUE = "videos.converted"
        HOST = "localhost"
        PORT = 5672

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=HOST,
                port=PORT,
            ),
        )
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE)

        message = {
            "error": "",
            "video": {
                "resource_id": f"{video_id}.VIDEO",
                "encoded_video_folder": "/path/to/encoded/video",
            },
            "status": "COMPLETED",
        }
        channel.basic_publish(exchange='', routing_key=QUEUE, body=json.dumps(message))

        print("Sent message")
        connection.close()
        