from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


class TestUpdateGenre:
    def test_update_genre_with_valid_categories(
        self,
    ):
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
        
        saved_action_genre = genre_repository.get_by_id(action_genre.id)
        saved_comedy_genre = genre_repository.get_by_id(comedy_genre.id)
        assert saved_action_genre == action_genre
        assert saved_comedy_genre == comedy_genre
        assert saved_action_genre.categories == {movie_category.id, documentary_category.id}
        assert saved_comedy_genre.categories == {movie_category.id}
        
        use_case = UpdateGenre(
            repository=genre_repository,
            category_repository=category_repository
        )
        
        use_case.execute(UpdateGenre.Input(id=action_genre.id,
                                            name="New Action",
                                            categories={movie_category.id},
                                            is_active=False))
        
        use_case.execute(UpdateGenre.Input(id=comedy_genre.id,
                                            name="New Comedy",
                                            categories=set(),
                                            is_active=False)) 
        
        output_action_genre_updated = genre_repository.get_by_id(action_genre.id)
        output_comedy_genre_updated = genre_repository.get_by_id(comedy_genre.id)
        
        assert output_action_genre_updated.name == "New Action"
        assert output_action_genre_updated.categories == {movie_category.id}
        assert output_action_genre_updated.is_active is False
        
        assert output_comedy_genre_updated.name == "New Comedy" 
        assert output_comedy_genre_updated.categories == set()
        assert output_comedy_genre_updated.is_active is False