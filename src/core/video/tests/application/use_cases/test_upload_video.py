from unittest.mock import create_autospec

from src.core.video.application.events.integration_events import AudioVideoMediaUpdatedIntegrationEvent
from src.core._shared.events.abstract_message_bus import AbstractMessageBus
from src.core._shared.infrastructure.storage.abstract_storage_service import AbstractStorageService
from src.core.video.application.use_cases.upload_video import UploadVideo
from src.core.video.infra.in_memory_video_repository import InMemoryVideoRepository
from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus, MediaType, Rating
from src.core.video.domain.video import Video


class TestUploadVideo:
    def test_upload_video_to_media(self):
        video =Video(
            title='My Video',
            description='my video description',
            launch_year=2025,
            duration=132,
            rating=Rating.L,
            opened=False,
            published=False,
            categories=set(),
            genres=set(),
            cast_members=set()
        )
        video_repository = InMemoryVideoRepository(videos=[video])
        mock_storage = create_autospec(AbstractStorageService)
        mock_message_bus = create_autospec(AbstractMessageBus)
        
        use_case = UploadVideo(
            video_repository=video_repository,
            storage_service=mock_storage,
            message_bus=mock_message_bus
        )
        
        input = UploadVideo.Input(
            video_id=video.id,
            file_name="video.mp4",
            content=b"video content",
            content_type="video/mp4",
        )
        
        use_case.execute(input=input)
        
        mock_storage.store.assert_called_once_with(
            file_path = f'videos/{str(video.id)}/video.mp4',
            content=b"video content",
            content_type="video/mp4"
        )
        
        video_from_repo = video_repository.get_by_id(video.id)
        video_from_repo.video == AudioVideoMedia(
            name='video.mp4',
            raw_location=f'videos/{str(video.id)}/video.mp4',
            encoded_location='',
            status=MediaStatus.PENDING,
            media_type=MediaType.VIDEO
        )
        
        mock_message_bus.handle.assert_called_once_with([
            AudioVideoMediaUpdatedIntegrationEvent(
                resource_id=f"{str(video.id)}.{MediaType.VIDEO}",
                file_path=f"videos/{video.id}/video.mp4",
            )
        ])
        
        
        
        
    def test_when_video_does_not_exist_then_raise_error(self):
        pass