from uuid import UUID, uuid4
from django.test import override_settings
from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.django_project.castmember_app.repository import DjangoORMCastMemberRepository
from src.core.castmember.domain.castmember import CastMember



@pytest.fixture
def actor_castmember() -> CastMember:
    return CastMember(
        name="Reinaldo",
        type='ACTOR'
    )


@pytest.fixture
def director_castmember() -> CastMember:
    return CastMember(
        name="Diana",
        type='DIRECTOR'
    )


@pytest.fixture
def castmember_repository() -> DjangoORMCastMemberRepository:
    return DjangoORMCastMemberRepository()


@pytest.mark.django_db
class TestListAPI:
    def test_list_castmember(
        self,
        actor_castmember: CastMember,
        director_castmember: CastMember,
        castmember_repository: DjangoORMCastMemberRepository
        
    ) -> None:
        
        castmember_repository.save(actor_castmember)
        castmember_repository.save(director_castmember)
        

        url = "/api/cast_members/"
        response = APIClient().get(url)

        expected_data = {
            "data": [
                            {
                "id": str(director_castmember.id),
                "name": director_castmember.name,
                "type": director_castmember.type,
            },
            {
                "id": str(actor_castmember.id),
                "name": actor_castmember.name,
                "type": actor_castmember.type,
            }
        ],
            'meta':{
                "current_page": 1,
                "total": 2,
                "per_page": 2
            }
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data


@pytest.mark.django_db
class TestCreateAPI:
    def test_create_castmember(
         self,
        actor_castmember: CastMember,
        director_castmember: CastMember,
        castmember_repository: DjangoORMCastMemberRepository
        
    ) -> None:
        

        url = "/api/cast_members/"

        data = {
            "name": "Ana",
            "type": 'ACTOR'
        }
        response = APIClient().post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"]
        created_castmember_id = UUID(response.data["id"])
        
        saved_castmember = castmember_repository.get_by_id(created_castmember_id)

        test_cast = CastMember(
            id=created_castmember_id,
            name="Ana",
            type='ACTOR'
        )

        assert saved_castmember.id == test_cast.id
        assert saved_castmember.name == test_cast.name
        assert test_cast.type == saved_castmember.type
    
    def test_create_castmember_invalid_type_return_400(
        self,
        castmember_repository: DjangoORMCastMemberRepository
    ) -> None:

        url = "/api/cast_members/"
        data = {
            "name": "Bruna",
            "type": 'Diretora'
        }
        response = APIClient().post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_create_castmember_invalid_name_return_400(
        self,
        castmember_repository: DjangoORMCastMemberRepository
    ) -> None:

        url = "/api/cast_members/"
        data = {
            "name": "",
            "type": 'ACTOR'
        }
        response = APIClient().post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestDeleteAPI:
    def test_delete_non_existent_castmember_raise_404(
        self
    ):
        url = f"/api/cast_members/{uuid4()}/"
        response = APIClient().delete(url)
        
        assert response.status_code == 404
    
    def test_delete_existent_genre(
        self,
        director_castmember: CastMember,
        castmember_repository: DjangoORMCastMemberRepository
    ):
        
        castmember_repository.save(director_castmember)
        
        url = f"/api/cast_members/{director_castmember.id}/"
        response = APIClient().delete(url)
        
        assert response.status_code == 204
        
    def test_delete_invalid_pk(
        self
    ):
        
        url = "/api/cast_members/ivalid-pk/"
        response = APIClient().delete(url)
        
        
        assert response.status_code == 400

@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_request_data_is_valid_then_update_castmember(
        self,
        actor_castmember: CastMember,
        director_castmember: CastMember,
        castmember_repository: DjangoORMCastMemberRepository
    ) -> None:
        castmember_repository.save(actor_castmember)
        saved_castmember = castmember_repository.get_by_id(actor_castmember.id)
        assert saved_castmember
        assert saved_castmember.name == "Reinaldo"
        
        
        url = f"/api/cast_members/{str(actor_castmember.id)}/"
        data = {
            "name": "Reinaldo 2",
            "type": 'DIRECTOR'
        }
        response = APIClient().put(url, data=data)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        updated_castmember = castmember_repository.get_by_id(actor_castmember.id)
        assert updated_castmember.name == 'Reinaldo 2'
        assert updated_castmember.type == 'DIRECTOR'
    
    def test_when_request_data_is_invalid_then_return_400(
        self,
        director_castmember: CastMember,
        castmember_repository: DjangoORMCastMemberRepository
    ) -> None:
        castmember_repository.save(director_castmember)
        saved_castmember = castmember_repository.get_by_id(director_castmember.id)
        assert saved_castmember
        assert saved_castmember.name == "Diana"
        
        url = f"/api/cast_members/{director_castmember.id}/"
        data = {
            "name": "",
            "type": 'DIRECTOR',
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"name": ["This field may not be blank."]}

    def test_when_type_do_not_exist_then_return_400(
        self,
        actor_castmember: CastMember,
        castmember_repository: DjangoORMCastMemberRepository
    ) -> None:
        castmember_repository.save(actor_castmember)

        url = f"/api/cast_members/{str(actor_castmember.id)}/"
        data = {
            "name": "Reinaldo 1",
            "type": 'Ator'
        }
        response = APIClient().put(url, data=data)

        print(response.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_when_castmember_does_not_exist_then_return_404(self) -> None:
        url = f"/api/cast_members/{str(uuid4())}/"
        data = {
            "name": "Diego",
            "type": 'ACTOR',
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        
         