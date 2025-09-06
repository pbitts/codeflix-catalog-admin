

from dataclasses import dataclass, field
from uuid import UUID

from src.core._shared.meta import ListOutputMeta
from src.core.genre.domain.genre_repository import GenreRepository


@dataclass
class GenreOutput:
    id: UUID
    name: str
    is_active: bool
    categories: set[UUID]

class ListGenre:
    def __init__(self, repository: GenreRepository):
        self.repository = repository
        
    
    @dataclass
    class Input:
        order_by : str = "name"
        current_page: int = 1
    
    @dataclass
    class Output:
        data: list[GenreOutput]
        meta: ListOutputMeta = field(default_factory=ListOutputMeta)
        
    def execute(self, input_data: Input) -> Output:
        genres = self.repository.list()
        
        sorted_genres = sorted([
                            GenreOutput(
                                id=genre.id,
                                name=genre.name,
                                is_active=genre.is_active,
                                categories=genre.categories
                            ) for genre in genres
                        ],
                        key=lambda genre: getattr(genre, input_data.order_by))
        
        DEFAULT_PAGE_SIZE = 2
        page_offset = (input_data.current_page - 1) * DEFAULT_PAGE_SIZE
        genres_page = sorted_genres[page_offset:page_offset + DEFAULT_PAGE_SIZE]
        

        return self.Output(data=genres_page,
                        meta=(ListOutputMeta(
                            current_page=input_data.current_page,
                            per_page=DEFAULT_PAGE_SIZE,
                            total=len(sorted_genres)
                        ))
                    )
        
        
        
        