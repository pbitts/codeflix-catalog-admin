from src.core._shared.meta import ListOutputMeta
from src.core.genre.application.use_cases.list_genre import GenreOutput, ListGenre
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


class TestListGenre:
    def test_list_genres_with_associated_categories(
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
        
        use_case = ListGenre(
            repository=genre_repository
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
                total=2
            )
        )
    
    def test_list_empty_genre_list(
        self,
    ):
        genre_repository = InMemoryGenreRepository()
        use_case = ListGenre(
            repository=genre_repository
        )
        
        output = use_case.execute(input_data=ListGenre.Input())
        
        assert len(output.data) == 0
        assert output == ListGenre.Output(data=[], meta=ListOutputMeta(current_page=1,
                                                      per_page=2,
                                                      total=0))