from dataclasses import dataclass
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.domain.genre_repository import GenreRepository



    
class UpdateGenre:
    
    def __init__(self, repository: GenreRepository, category_repository: CategoryRepository):
        self.repository = repository
        self.category_repository = category_repository
        
    @dataclass
    class Input:
        id: UUID
        name: str
        categories: set[UUID]
        is_active: bool

    def execute(self, input: Input) -> None:
        genre = self.repository.get_by_id(input.id)
        if not genre:
            raise GenreNotFound(f"Genre with id {input.id} not found")
        
        category_ids = {category.id for category in self.category_repository.list()}
        if not input.categories.issubset(category_ids):
            raise RelatedCategoriesNotFound(
                f"Categories not found: {input.categories - category_ids}"
            )
        
        try:    
            if input.is_active is True:
                genre.activate()
            if input.is_active is False:
                genre.deactivate()
            
            genre.change_name(name=input.name)
            genre.update_categories(categories=input.categories)
        except ValueError as err:
            raise InvalidGenre(err)

        self.repository.update(genre)
        
        