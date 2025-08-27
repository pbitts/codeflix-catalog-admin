import pytest

from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.core.genre.domain.genre import Genre
from src.django_project.genre_app.models import Genre as GenreModel
from src.django_project.genre_app.repository import DjangoORMGenreRepository


@pytest.mark.django_db
class TestSave:
    def test_save_genre_in_db(self):
        repository = DjangoORMGenreRepository()
        genre = Genre(name="Action")
        
        GenreModel.objects.count() == 0
        repository.save(genre)
        
        assert GenreModel.objects.count() == 1
        genre_model = GenreModel.objects.get(id=genre.id)
        assert genre_model.id == genre.id
        assert genre_model.name == "Action"
        assert genre_model.is_active is True
        assert list(genre_model.categories.all()) == []
    
    def test_save_genre_with_categories_in_db(self):
        repository = DjangoORMGenreRepository()
        category_repository = DjangoORMCategoryRepository()
        
        category= Category(name='Movie')
        category_repository.save(category)
        
        genre = Genre(name="Action")
        genre.add_category(category.id)
        
        assert GenreModel.objects.count() == 0
        repository.save(genre)
        
        assert GenreModel.objects.count() == 1
        genre_model = GenreModel.objects.get(id=genre.id)
        related_category = genre_model.categories.first()
        assert related_category.id == category.id
        assert genre_model.name == "Action"