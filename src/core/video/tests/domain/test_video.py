import pytest
from decimal import Decimal
from uuid import uuid4
from src.core.video.domain.video import Video
from src.core.video.domain.value_objects import Rating


class TestCreateVideo:
    def test_video_creation_success(self):
        video = Video(
            title="Valid Title",
            description="Some description",
            launch_year=2025,
            duration=Decimal("120.0"),
            published=True,
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
                rating=Rating.L,
                categories=set(),
                genres=set(),
                cast_members=set()
            )
        assert "title cannot be longer than 255" in str(exc_info.value)