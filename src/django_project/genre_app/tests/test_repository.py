import uuid
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


@pytest.mark.django_db
class TestList:
    def test_list_genres(self):
        repository = DjangoORMGenreRepository()
        genre1 = Genre(name="Action")
        genre2 = Genre(name="Horror", is_active=False)
        
        repository.save(genre1)
        repository.save(genre2)
        
        genres = repository.list()
        
        assert len(genres) == 2
        assert genres[0].id == genre1.id
        assert genres[0].name == "Action"
        assert genres[0].is_active is True
        
        assert genres[1].id == genre2.id
        assert genres[1].name == "Horror"
        assert genres[1].is_active is False
        
        
@pytest.mark.django_db
class TestGetById:
    def test_get_genre_by_id(self):
        repository = DjangoORMGenreRepository()
        genre = Genre(name="Action")
        
        repository.save(genre)
        
        found_genre = repository.get_by_id(genre.id)
        
        assert found_genre is not None
        assert found_genre.id == genre.id
        assert found_genre.name == "Action"
        assert found_genre.is_active is True
    
    def test_get_genre_by_id_not_found(self):
        repository = DjangoORMGenreRepository()
        
        found_genre = repository.get_by_id(uuid.uuid4())
        
        assert found_genre is None
        

@pytest.mark.django_db
class TestUpdate:
    def test_update_genre(self):
        repository = DjangoORMGenreRepository()
        category_repository = DjangoORMCategoryRepository()
        
        category1 = Category(name='Movie')
        category2 = Category(name='Documentary')
        category_repository.save(category1)
        category_repository.save(category2)
        
        genre = Genre(name="Action")
        genre.add_category(category1.id)
        repository.save(genre)
        
        # Update genre details
        genre.name = "Action Updated"
        genre.is_active = False
        genre.add_category(category2.id)
        
        repository.update(genre)
        
        updated_genre_model = GenreModel.objects.get(id=genre.id)
        
        assert updated_genre_model.name == "Action Updated"
        assert updated_genre_model.is_active is False
        related_categories = list(updated_genre_model.categories.all())
        assert len(related_categories) == 2
        assert category1.id in [cat.id for cat in related_categories]
        assert category2.id in [cat.id for cat in related_categories]
    
    def test_update_genre_not_found(self):
        repository = DjangoORMGenreRepository()
        
        genre = Genre(name="Non-existent")
        
        result = repository.update(genre)
        
        assert result is None
        
@pytest.mark.django_db
class TestDelete:
    def test_delete_genre(self):
        repository = DjangoORMGenreRepository()
        genre = Genre(name="Action")
        
        repository.save(genre)
        
        assert GenreModel.objects.count() == 1
        
        repository.delete(genre.id)
        
        assert GenreModel.objects.count() == 0
    
    def test_delete_genre_not_found(self):
        repository = DjangoORMGenreRepository()
        repository = DjangoORMGenreRepository()
        genre = Genre(name="Action")
        
        repository.save(genre)
        assert GenreModel.objects.count() == 1
        
        repository.delete(uuid.uuid4())
        
        assert GenreModel.objects.count() == 1
        assert GenreModel.objects.get(id=genre.id) is not None