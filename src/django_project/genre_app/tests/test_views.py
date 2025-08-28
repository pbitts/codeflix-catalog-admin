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
def category_repository(category_documentary, category_movie) -> DjangoORMCategoryRepository:
    repo = DjangoORMCategoryRepository()
    repo.save(category_documentary)
    repo.save(category_movie)
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


@pytest.mark.django_db
class TestCreateAPI:
    def test_create_genre_with_categories(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
        genre_repository: DjangoORMGenreRepository,
    ) -> None:

        url = "/api/genres/"
        data = {
            "name": "Romance",
            "is_active": True,
            "categories": [str(category_movie.id), str(category_documentary.id)],
        }
        response = APIClient().post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"]
        created_genre_id = UUID(response.data["id"])
        
        saved_genre = genre_repository.get_by_id(created_genre_id)
        assert saved_genre == Genre(
            id=UUID(response.data["id"]),
            name="Romance",
            is_active=True,
            categories={category_movie.id, category_documentary.id}
        )
    
    def test_create_genre_invalid_categories_return_400(
        self,
        category_repository: DjangoORMCategoryRepository,
        genre_repository: DjangoORMGenreRepository,
    ) -> None:

        url = "/api/genres/"
        data = {
            "name": "Romance",
            "is_active": True,
            "categories": [str(uuid4())],
        }
        response = APIClient().post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_create_genre_invalid_name_return_400(
        self,
        category_repository: DjangoORMCategoryRepository,
        genre_repository: DjangoORMGenreRepository,
        category_movie: Category
    ) -> None:

        url = "/api/genres/"
        data = {
            "name": "",
            "is_active": True,
            "categories": [str(category_movie.id)],
        }
        response = APIClient().post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestDeleteAPI:
    def test_delete_non_existent_genre_raise_404(
        self
    ):
        url = f"/api/genres/{uuid4()}/"
        response = APIClient().delete(url)
        
        assert response.status_code == 404
    
    def test_delete_existent_genre(
        self,
        genre_drama: Genre,
        genre_repository: DjangoORMCategoryRepository
    ):
        
        genre_repository.save(genre_drama)
        
        url = f"/api/genres/{genre_drama.id}/"
        response = APIClient().delete(url)
        
        assert response.status_code == 204
        
    def test_delete_invalid_pk(
        self
    ):
        
        url = "/api/genres/ivalid-pk/"
        response = APIClient().delete(url)
        
        
        assert response.status_code == 400

@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_request_data_is_valid_then_update_genre(
        self,
        category_repository: DjangoORMCategoryRepository,
        category_movie: Category,
        category_documentary: Category,
        genre_repository: DjangoORMGenreRepository,
        genre_romance: Genre
    ) -> None:
        genre_repository.save(genre_romance)
        saved_genre = genre_repository.get_by_id(genre_romance.id)
        assert saved_genre
        assert saved_genre.name == "Romance"
        
        
        url = f"/api/genres/{str(genre_romance.id)}/"
        data = {
            "name": "Drama",
            "is_active": True,
            "categories": [category_documentary.id]
        }
        response = APIClient().put(url, data=data)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        updated_genre = genre_repository.get_by_id(genre_romance.id)
        assert updated_genre.name == 'Drama'
        assert updated_genre.is_active is True
        assert updated_genre.categories == {category_documentary.id}
    
    def test_when_request_data_is_invalid_then_return_400(
        self,
        genre_drama: Genre,
    ) -> None:
        url = f"/api/genres/{str(genre_drama.id)}/"
        data = {
            "name": "",
            "is_active": True,
            "categories": [],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"name": ["This field may not be blank."]}

    def test_when_related_categories_do_not_exist_then_return_400(
        self,
        category_repository: DjangoORMCategoryRepository,
        category_movie: Category,
        category_documentary: Category,
        genre_repository: DjangoORMGenreRepository,
        genre_romance: Genre,
    ) -> None:
        genre_repository.save(genre_romance)

        url = f"/api/genres/{str(genre_romance.id)}/"
        data = {
            "name": "Romance",
            "is_active": True,
            "categories": [uuid4()],  # non-existent category
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Categories with provided IDs not found" in response.data["error"]

    def test_when_genre_does_not_exist_then_return_404(self) -> None:
        url = f"/api/genres/{str(uuid4())}/"
        data = {
            "name": "Romance",
            "is_active": True,
            "categories": [],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        
         