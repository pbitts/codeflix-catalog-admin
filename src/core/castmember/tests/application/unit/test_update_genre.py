from unittest.mock import create_autospec
from uuid import uuid4

import pytest
from src.core.genre.domain.genre import Genre
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.application.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound


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
        
class TestUpdateGenre:
    def test_update_non_existent_genre_raises_genre_not_found(
        self,
        mock_genre_repository: GenreRepository,
        mock_category_repository_with_categories: CategoryRepository
    ):
        
        mock_genre_repository.get_by_id.return_value = None
        
        use_case = UpdateGenre(
            repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories
        )
        
        fake_id = uuid4()
        with pytest.raises(GenreNotFound):
            use_case.execute(input=UpdateGenre.Input(id=fake_id, name='Romance',   categories=set(), is_active=True))
        
        mock_genre_repository.get_by_id.assert_called_once_with(fake_id)
    
    def test_update_genre_with_invalid_data_raises_invalid_genre(
        self,
        mock_genre_repository: GenreRepository,
        mock_empty_category_repository: CategoryRepository
    ):
        
        existing_genre = Genre(name="Action")
        
        mock_genre_repository.get_by_id.return_value = existing_genre
        
        use_case = UpdateGenre(
            repository=mock_genre_repository,
            category_repository=mock_empty_category_repository
        )
        
        with pytest.raises(InvalidGenre):
            use_case.execute(input=UpdateGenre.Input(
                id=existing_genre.id,
                name="",  # Invalid name
                categories=set(),
                is_active=True
            ))
        
        mock_genre_repository.get_by_id.assert_called_once_with(existing_genre.id)
        mock_genre_repository.update.assert_not_called()
        
    def test_update_genre_with_non_existent_categories_raises_related_categories_not_found(
        self,
        mock_genre_repository: GenreRepository,
        mock_empty_category_repository: CategoryRepository
    ):
        from src.core.genre.domain.genre import Genre
        
        existing_genre = Genre(name="Action")
        
        mock_genre_repository.get_by_id.return_value = existing_genre
        
        use_case = UpdateGenre(
            repository=mock_genre_repository,
            category_repository=mock_empty_category_repository
        )
        
        non_existent_category_id = uuid4()
        
        with pytest.raises(RelatedCategoriesNotFound):
            use_case.execute(input=UpdateGenre.Input(
                id=existing_genre.id,
                name="Adventure",
                categories={non_existent_category_id},  # Non-existent category
                is_active=True
            ))
        
        mock_genre_repository.get_by_id.assert_called_once_with(existing_genre.id)
        mock_genre_repository.update.assert_not_called()
    
    def test_successful_genre_update(
        self,
        mock_genre_repository: GenreRepository,
        mock_category_repository_with_categories: CategoryRepository,
        movie_category: Category,
        documentary_category: Category
    ):
        
        existing_genre = Genre(name="Action", is_active=False)
        
        mock_genre_repository.get_by_id.return_value = existing_genre
        
        use_case = UpdateGenre(
            repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories
        )
        
        new_name = "Adventure"
        new_categories = {movie_category.id, documentary_category.id}
        
        use_case.execute(input=UpdateGenre.Input(
            id=existing_genre.id,
            name=new_name,
            categories=new_categories,
            is_active=False
        ))
        mock_genre_repository.get_by_id.assert_called_once_with(existing_genre.id)
        mock_genre_repository.update.assert_called_once()
