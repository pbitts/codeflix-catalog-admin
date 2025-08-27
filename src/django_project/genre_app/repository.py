from django.db import transaction

from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository
from src.django_project.genre_app.models import Genre as GenreModel

class DjangoORMGenreRepository(GenreRepository):
    
    def save(self, genre: Genre):
        with transaction.atomic():
            genre_model = GenreModel.objects.create(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active,
            )
            genre_model.categories.set(genre.categories)
    
    def get_by_id(self, genre_id: str) -> Genre:
        pass
    
    def list(self) -> list[Genre]:
        pass
    
    def update(self, genre: Genre):
        pass
    
    def delete(self, genre_id: str):
        pass