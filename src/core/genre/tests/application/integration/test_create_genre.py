import uuid
import pytest

from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.application.exceptions import RelatedCategoriesNotFound
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")

@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")
    
@pytest.fixture
def category_repository(movie_category, documentary_category) -> CategoryRepository:
    return InMemoryCategoryRepository(
        categories=[movie_category, documentary_category]
    )

class TestCreateGenre:
    def test_create_genre_with_associated_categories(
        self,
        movie_category,
        documentary_category,
        category_repository,
    ):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(
            repository=genre_repository,
            category_repository=category_repository
        )
        input = CreateGenre.Input(
            name="Action",
            categories={movie_category.id, documentary_category.id}
        )
        
        output = use_case.execute(input)
        
        assert isinstance(output, CreateGenre.Output)
        assert isinstance(output.id, uuid.UUID)
        assert len(genre_repository.genres) == 1
        genre = genre_repository.get_by_id(output.id)
        assert genre.id == output.id
        assert genre.name == "Action"
        assert genre.is_active is True
        assert genre.categories == {movie_category.id, documentary_category.id}
    
    def test_create_genre_with_inexistent_categories_raise_an_error(
        self,
        category_repository,
    ):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(
            repository=genre_repository,
            category_repository=category_repository
        )
        input = CreateGenre.Input(
            name="Action",
            categories={uuid.uuid4(), uuid.uuid4()}
        )
        
        with pytest.raises(RelatedCategoriesNotFound) as exc_info:
            use_case.execute(input)
        
        assert "Categories with provided IDs not found" in str(exc_info.value)
        assert len(genre_repository.genres) == 0
        
    def test_create_genre_without_categories(
        self,
        category_repository,
    ):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(
            repository=genre_repository,
            category_repository=category_repository
        )
        input = CreateGenre.Input(
            name="Action",
        )
        
        output = use_case.execute(input)
        
        assert isinstance(output, CreateGenre.Output)
        assert isinstance(output.id, uuid.UUID)
        assert len(genre_repository.genres) == 1
        genre = genre_repository.get_by_id(output.id)
        assert genre.id == output.id
        assert genre.name == "Action"
        assert genre.is_active is True
        assert genre.categories == set()