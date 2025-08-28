from uuid import UUID
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
    
    def get_by_id(self, id: UUID) -> Genre:
        try:
            genre_model = GenreModel.objects.get(id=id)
        except GenreModel.DoesNotExist:
            return None
        return Genre(
            id=genre_model.id,
            name=genre_model.name,
            is_active=genre_model.is_active,
            categories={cat.id for cat in genre_model.categories.all()}
        )
    
    def list(self) -> list[Genre]:
        return [
            Genre(
                id=genre_model.id,
                name=genre_model.name,
                is_active=genre_model.is_active,
                categories={cat.id for cat in genre_model.categories.all()}
            )
            for genre_model in GenreModel.objects.all()
        ]
    
    def update(self, genre: Genre) -> None:
        try:
            genre_model = GenreModel.objects.get(id=genre.id)
        except GenreModel.DoesNotExist:
            return None
        
        with transaction.atomic():
            GenreModel.objects.filter(id=genre.id).update(
                name=genre.name,
                is_active=genre.is_active,
            )
            # Sets a final state to the categories relation
            genre_model.categories.set(genre.categories)
    
    def delete(self, id: UUID) -> None:
        GenreModel.objects.filter(id=id).delete()