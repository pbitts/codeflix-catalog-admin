from unittest.mock import create_autospec
import pytest

from src.core._shared.meta import ListOutputMeta
from src.core.genre.application.use_cases.list_genre import GenreOutput, ListGenre
from src.core.genre.domain.genre import Genre
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.domain.genre_repository import GenreRepository

@pytest.fixture
def mock_genre_repository() -> GenreRepository:
    return create_autospec(GenreRepository)

@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")

@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")

@pytest.fixture
def mock_category_repository_with_categories(
    movie_category: Category,
    documentary_category: Category
) -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value =[movie_category, documentary_category]
    return repository

@pytest.fixture
def mock_empty_category_repository() -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = []
    return repository
    

class TestListGenre:
    def test_when_no_genres_exist_then_return_empty_list(
        self,
        mock_genre_repository: GenreRepository
    ):
        mock_genre_repository.list.return_value = []
        
        use_case = ListGenre(
            repository=mock_genre_repository
        )
        
        output = use_case.execute(input_data=ListGenre.Input())
        
        assert output == ListGenre.Output(data=[], meta=ListOutputMeta(
                                                      current_page=1,
                                                      per_page=2,
                                                      total=0))
        mock_genre_repository.list.assert_called_once()
    
    def test_when_genres_exist_then_return_genre_list(
        self,
        mock_genre_repository: GenreRepository,
        movie_category: Category,
        documentary_category: Category
    ):
        action_genre = Genre(
            name="Action",
            categories={movie_category.id, documentary_category.id}
        )
        comedy_genre = Genre(
            name="Comedy",
            categories={movie_category.id}
        )
        mock_genre_repository.list.return_value = [action_genre, comedy_genre]
        
        use_case = ListGenre(
            repository=mock_genre_repository
        )
        
        output = use_case.execute(input_data=ListGenre.Input())
        
        assert len(output.data) == 2
        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    id=action_genre.id,
                    name=action_genre.name,
                    is_active=action_genre.is_active,
                    categories=action_genre.categories
                ),
                GenreOutput(
                    id=comedy_genre.id,
                    name=comedy_genre.name,
                    is_active=comedy_genre.is_active,
                    categories=comedy_genre.categories
                )
            ],
            meta=ListOutputMeta(
                                current_page=1,
                                per_page=2,
                                total=2)
        )
        mock_genre_repository.list.assert_called_once()
    
            