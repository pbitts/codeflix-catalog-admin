

from decimal import Decimal
from unittest.mock import create_autospec
import uuid
import pytest

from src.core.video.application.exceptions import RelatedEntitiesNotFound
from src.core.video.application.use_cases.create_video_without_media import CreateVideoWithoutMedia
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository
from src.core.castmember.domain.castmember_repository import CastMemberRepository
from src.core.castmember.domain.castmember import CastMember
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


@pytest.fixture
def romance_genre() -> Genre:
    return Genre(name='Romance')

@pytest.fixture
def mock_genre_repository(
    romance_genre
    ) -> GenreRepository:
    repository = create_autospec(GenreRepository)
    repository.list.return_value =[romance_genre]
    return repository 

@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")

@pytest.fixture
def mock_category_repository(
    movie_category
) -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value =[movie_category]
    return repository

@pytest.fixture
def actor_castmember() -> CastMember:
    return CastMember(name="Alice", type='ACTOR')

@pytest.fixture
def mock_castmember_repository(
    actor_castmember
) -> CastMemberRepository:
    repository = create_autospec(CastMemberRepository)
    repository.list.return_value =[actor_castmember]
    return repository

@pytest.fixture
def mock_video_repository() -> VideoRepository:
    return create_autospec(VideoRepository)


class TestCreateVideoWithoutMedia:
    def test_create_video_without_media_and_no_categories_cast_members_nor_genre(
        self, mock_video_repository, mock_category_repository, mock_genre_repository, mock_castmember_repository
    ):
        usecase = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_genre_repository,
            castmember_repository=mock_castmember_repository,
        )

        input_data = CreateVideoWithoutMedia.Input(
            title="My Movie",
            description="A simple test movie",
            launch_year=2023,
            duration=Decimal("120.5"),
            rating="G",
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        output = usecase.execute(input_data)

        mock_video_repository.save.assert_called_once()
        assert isinstance(output.id, uuid.UUID)
    
    def test_create_video_without_media_and_with_category_castmember_and_genre(
        self, mock_video_repository, movie_category, actor_castmember, romance_genre,
        mock_category_repository, mock_castmember_repository, mock_genre_repository
    ):
        usecase = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_genre_repository,
            castmember_repository=mock_castmember_repository,
        )

        input_data = CreateVideoWithoutMedia.Input(
            title="Romantic Drama",
            description="A love story",
            launch_year=2024,
            duration=Decimal("90.0"),
            rating="PG",
            categories={movie_category.id},
            genres={romance_genre.id},
            cast_members={actor_castmember.id},
        )

        output = usecase.execute(input_data)

        mock_video_repository.save.assert_called_once()
        assert isinstance(output.id, uuid.UUID)
    
    def test_create_video_without_media_and_with_category_castmember_but_invalid_genre(
        self, mock_video_repository, movie_category, actor_castmember,
        mock_category_repository, mock_castmember_repository, mock_genre_repository
    ):
        usecase = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_genre_repository,
            castmember_repository=mock_castmember_repository,
        )

        invalid_genre_id = uuid.uuid4()
        input_data = CreateVideoWithoutMedia.Input(
            title="Invalid Genre Movie",
            description="Should fail due to genre",
            launch_year=2025,
            duration=Decimal("100.0"),
            rating="PG",
            categories={movie_category.id},
            genres={invalid_genre_id},
            cast_members={actor_castmember.id},
        )

        with pytest.raises(RelatedEntitiesNotFound) as exc:
            usecase.execute(input_data)

        assert str(invalid_genre_id) in str(exc.value)
    
    def test_create_video_without_media_and_with_category_genre_but_invalid_castmember(
        self, mock_video_repository, movie_category, romance_genre,
        mock_category_repository, mock_castmember_repository, mock_genre_repository
    ):
        usecase = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_genre_repository,
            castmember_repository=mock_castmember_repository,
        )

        invalid_castmember_id = uuid.uuid4()
        input_data = CreateVideoWithoutMedia.Input(
            title="Invalid Cast Movie",
            description="Should fail due to castmember",
            launch_year=2025,
            duration=Decimal("110.0"),
            rating="PG-13",
            categories={movie_category.id},
            genres={romance_genre.id},
            cast_members={invalid_castmember_id},
        )

        with pytest.raises(RelatedEntitiesNotFound) as exc:
            usecase.execute(input_data)

        assert str(invalid_castmember_id) in str(exc.value)
    
    def test_create_video_without_media_and_with_genre_castmember_but_invalid_category(
        self, mock_video_repository, actor_castmember, romance_genre,
        mock_category_repository, mock_castmember_repository, mock_genre_repository
    ):
        usecase = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_genre_repository,
            castmember_repository=mock_castmember_repository,
        )

        invalid_category_id = uuid.uuid4()
        input_data = CreateVideoWithoutMedia.Input(
            title="Invalid Category Movie",
            description="Should fail due to category",
            launch_year=2025,
            duration=Decimal("130.0"),
            rating="R",
            categories={invalid_category_id},
            genres={romance_genre.id},
            cast_members={actor_castmember.id},
        )

        with pytest.raises(RelatedEntitiesNotFound) as exc:
            usecase.execute(input_data)

        assert str(invalid_category_id) in str(exc.value)
    
    def test_create_video_without_media_and_with_genre_but_invalid_category_and_invalid_castmember(
        self, mock_video_repository, romance_genre,
        mock_category_repository, mock_castmember_repository, mock_genre_repository
    ):
        usecase = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_genre_repository,
            castmember_repository=mock_castmember_repository,
        )

        invalid_category_id = uuid.uuid4()
        invalid_castmember_id = uuid.uuid4()
        input_data = CreateVideoWithoutMedia.Input(
            title="Invalid Category and Cast",
            description="Should fail due to category and castmember",
            launch_year=2025,
            duration=Decimal("95.0"),
            rating="PG",
            categories={invalid_category_id},
            genres={romance_genre.id},
            cast_members={invalid_castmember_id},
        )

        with pytest.raises(RelatedEntitiesNotFound) as exc:
            usecase.execute(input_data)

        error_message = str(exc.value)
        assert str(invalid_category_id) in error_message
        assert str(invalid_castmember_id) in error_message