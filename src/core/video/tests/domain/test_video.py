import pytest
from decimal import Decimal
from uuid import uuid4
from src.core.video.domain.video import Video
from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus, MediaType, Rating


class TestCreateVideo:
    def test_video_creation_success(self):
        video = Video(
            title="Valid Title",
            description="Some description",
            launch_year=2025,
            duration=Decimal("120.0"),
            published=True,
            opened=False,
            rating=Rating.L,  
            categories= set(),
            genres= set(),
            cast_members=set())
            
        assert video.title == "Valid Title"
        assert video.published is True
        assert video.duration == Decimal("120.0")
        assert isinstance(video.categories, set)
        assert isinstance(video.genres, set)
        assert isinstance(video.cast_members, set)

    def test_video_creation_empty_title_raises(self):
        with pytest.raises(ValueError) as exc_info:
            Video(
                title="",
                description="Some description",
                launch_year=2025,
                duration=Decimal("90.0"),
                published=False,
                opened=False,
                rating=Rating.L,
                categories=set(),
                genres=set(),
                cast_members=set()
            )
        assert "title cannot be empty" in str(exc_info.value)

    def test_video_creation_title_too_long_raises(self):
        long_title = "A" * 256
        with pytest.raises(ValueError) as exc_info:
            Video(
                title=long_title,
                description="Some description",
                launch_year=2025,
                duration=Decimal("90.0"),
                published=False,
                opened=False,
                rating=Rating.L,
                categories=set(),
                genres=set(),
                cast_members=set()
            )
        assert "title cannot be longer than 255" in str(exc_info.value)
        

class TestVideoProcess:
    def make_video_with_media(self):
        video = Video(
            title="Test Video",
            description="desc",
            launch_year=2025,
            duration=Decimal("100.0"),
            published=False,
            opened=False,
            rating=Rating.L,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        video.video = AudioVideoMedia(
            name="raw_video.mp4",
            raw_location="/tmp/raw.mp4",
            media_type=MediaType.VIDEO,
            encoded_location="",
            status=MediaStatus.PROCESSING,
        )
        return video

    def test_process_completed_updates_video_and_publishes(self):
        video = self.make_video_with_media()
        encoded_path = "/encoded/video.mp4"

        video.process(MediaStatus.COMPLETED, encoded_path)

        assert video.video.status == MediaStatus.COMPLETED
        assert video.video.encoded_location == encoded_path
        assert video.published is True  # publish() deve ter sido chamado

    def test_process_error_sets_status_error_and_empty_encoded_location(self):
        video = self.make_video_with_media()

        video.process(MediaStatus.ERROR, "/does/not/matter.mp4")

        assert video.video.status == MediaStatus.ERROR
        assert video.video.encoded_location == ""
        assert video.published is False