import uuid

import pytest
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.application.exceptions import GenreNotFound
from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository
from src.core.category.domain.category import Category


class TestDeleteGenre:
    def test_delete_genre(self):
  
        category_repository = InMemoryCategoryRepository()
        movie_category = Category(name="Movie")
        documentary_category = Category(name="Documentary")
        category_repository.save(movie_category)
        category_repository.save(documentary_category)
        
        genre_repository = InMemoryGenreRepository()
        action_genre = Genre(
            name="Action",
            categories={movie_category.id, documentary_category.id}
        )
        comedy_genre = Genre(
            name="Comedy",
            categories={movie_category.id}
        )
        genre_repository.save(action_genre)
        genre_repository.save(comedy_genre)
        
        use_case = DeleteGenre(
            repository=genre_repository
        )
        
        output = use_case.execute(input=DeleteGenre.Input(id=action_genre.id))
        assert output is None
        assert genre_repository.list() == [comedy_genre]
        
    def test_delete_genre_not_found(self):
        genre_repository = InMemoryGenreRepository()
        use_case = DeleteGenre(
            repository=genre_repository
        )
        
        with pytest.raises(GenreNotFound):
            use_case.execute(input=DeleteGenre.Input(id=uuid.uuid4()))