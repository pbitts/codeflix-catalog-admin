from uuid import UUID, uuid4
from django.test import override_settings
from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre

from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository


@pytest.fixture
def category_movie():
    return Category(
        name="Movie",
        description="Movie description",
    )


@pytest.fixture
def category_documentary():
    return Category(
        name="Documentary",
        description="Documentary description",
    )


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    repo = DjangoORMCategoryRepository()
    return repo

@pytest.fixture
def genre_romance(category_movie, category_documentary) -> Genre:
    return Genre(
        name="Romance",
        is_active=True,
        categories={category_documentary.id, category_movie.id},
    )


@pytest.fixture
def genre_drama() -> Genre:
    return Genre(
        name="Drama",
        is_active=True,
        categories=set(),
    )


@pytest.fixture
def genre_repository() -> DjangoORMGenreRepository:
    return DjangoORMGenreRepository()


@pytest.mark.django_db
class TestListAPI:
    def test_list_genres_and_categories(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
        genre_romance: Genre,
        genre_drama: Genre,
        genre_repository: DjangoORMGenreRepository,
    ) -> None:
        
        category_repository.save(category_documentary)
        category_repository.save(category_movie)
        
        genre_repository.save(genre_romance)
        genre_repository.save(genre_drama)
        

        url = "/api/genres/"
        response = APIClient().get(url)

        # TODO: Quando implementarmos ordenação, poderemos comparar expected_data
        # expected_data = {
        #     "data": [
        #         {
        #             "id": str(genre_romance.id),
        #             "name": "Romance",
        #             "is_active": True,
        #             "categories": [
        #                 str(category_documentary.id),
        #                 str(category_movie.id),
        #             ],
        #         },
        #         {
        #             "id": str(genre_drama.id),
        #             "name": "Drama",
        #             "is_active": True,
        #             "categories": [],
        #         },
        #     ]
        # }
        
        # assert response.data == expected_data
        print(response.data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]
        assert response.data["data"][0]["id"] == str(genre_romance.id)
        assert response.data["data"][0]["name"] == "Romance"
        assert response.data["data"][0]["is_active"] is True
        assert set(response.data["data"][0]["categories"]) == {
            str(category_documentary.id),
            str(category_movie.id),
        }
        assert response.data["data"][1]["id"] == str(genre_drama.id)
        assert response.data["data"][1]["name"] == "Drama"
        assert response.data["data"][1]["is_active"] is True
        assert response.data["data"][1]["categories"] == []

