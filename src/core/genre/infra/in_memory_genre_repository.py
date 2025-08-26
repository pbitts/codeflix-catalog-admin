from uuid import UUID

from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.domain.genre import Genre


class InMemoryGenreRepository(GenreRepository):
    def __init__(self, genres=None):
        self.genres = genres or []
    
    def save(self, genre):
        self.genres.append(genre)
    
    def get_by_id(self, id: UUID) -> Genre | None:
        return next((Genre for Genre in self.genres if Genre.id == id), None)
    
    def delete(self, id: UUID) -> None:
        Genre = self.get_by_id(id)
        self.genres.remove(Genre)
    
    def update(self, genre: Genre) -> None:
        old_genre = self.get_by_id(genre.id) 
        if old_genre:
            self.genres.remove(old_genre)
            self.genres.append(Genre)
    
    def list(self) -> list[Genre]:
        # Return a copy of the genre list to avoid external modifications
        return [genre for genre in self.genres]