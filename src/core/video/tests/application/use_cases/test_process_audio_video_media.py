import pytest
from unittest.mock import create_autospec
import uuid
from decimal import Decimal

from src.core.video.application.use_cases.process_audio_video_media import ProcessAudioVideoMedia
from src.core.video.application.exceptions import VideoNotFound, MediaNotFound
from src.core.video.domain.video_repository import VideoRepository
from src.core.video.domain.video import Video
from src.core.video.domain.value_objects import (
    MediaStatus,
    MediaType,
    AudioVideoMedia,
    Rating,
)


@pytest.fixture
def mock_video_repository() -> VideoRepository:
    return create_autospec(VideoRepository)


@pytest.fixture
def sample_video() -> Video:
    return Video(
        title="Sample",
        description="desc",
        launch_year=2025,
        duration=Decimal("120.0"),
        opened=False,
        published=False,
        rating=Rating.L,
        categories=set(),
        genres=set(),
        cast_members=set(),
    )


class TestProcessAudioVideoMedia:
    def test_video_not_found_raises(self, mock_video_repository):
        usecase = ProcessAudioVideoMedia(mock_video_repository)
        input_data = ProcessAudioVideoMedia.Input(
            encoded_location="/encoded/file.mp4",
            video_id=uuid.uuid4(),
            status=MediaStatus.COMPLETED,
            media_type=MediaType.VIDEO,
        )
        mock_video_repository.get_by_id.return_value = None

        with pytest.raises(VideoNotFound):
            usecase.execute(input_data)

    def test_video_has_no_media_raises(self, mock_video_repository, sample_video):
        usecase = ProcessAudioVideoMedia(mock_video_repository)
        input_data = ProcessAudioVideoMedia.Input(
            encoded_location="/encoded/file.mp4",
            video_id=uuid.uuid4(),
            status=MediaStatus.COMPLETED,
            media_type=MediaType.VIDEO,
        )
        mock_video_repository.get_by_id.return_value = sample_video
        sample_video.video = None  # sem mídia associada

        with pytest.raises(MediaNotFound):
            usecase.execute(input_data)

    def test_process_completed_updates_video(self, mock_video_repository, sample_video):
        usecase = ProcessAudioVideoMedia(mock_video_repository)
        sample_video.video = AudioVideoMedia(
            name="raw.mp4",
            raw_location="/tmp/raw.mp4",
            media_type=MediaType.VIDEO,
            encoded_location="",
            status=MediaStatus.PROCESSING,
        )
        mock_video_repository.get_by_id.return_value = sample_video

        input_data = ProcessAudioVideoMedia.Input(
            encoded_location="/encoded/file.mp4",
            video_id=uuid.uuid4(),
            status=MediaStatus.COMPLETED,
            media_type=MediaType.VIDEO,
        )

        usecase.execute(input_data)

        mock_video_repository.update.assert_called_once_with(sample_video)
        assert sample_video.video.status == MediaStatus.COMPLETED
        assert sample_video.video.encoded_location == "/encoded/file.mp4"

    def test_process_error_updates_video_as_error(self, mock_video_repository, sample_video):
        usecase = ProcessAudioVideoMedia(mock_video_repository)
        sample_video.video = AudioVideoMedia(
            name="raw.mp4",
            raw_location="/tmp/raw.mp4",
            media_type=MediaType.VIDEO,
            encoded_location="",
            status=MediaStatus.PROCESSING,
        )
        mock_video_repository.get_by_id.return_value = sample_video

        input_data = ProcessAudioVideoMedia.Input(
            encoded_location="/encoded/file.mp4",  # não será usado em erro
            video_id=uuid.uuid4(),
            status=MediaStatus.ERROR,
            media_type=MediaType.VIDEO,
        )

        usecase.execute(input_data)

        mock_video_repository.update.assert_called_once_with(sample_video)
        assert sample_video.video.status == MediaStatus.ERROR
        assert sample_video.video.encoded_location == ""
