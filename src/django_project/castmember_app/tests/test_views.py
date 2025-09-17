import datetime
import os
from uuid import UUID, uuid4

import dotenv
import jwt
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.django_project.castmember_app.repository import DjangoORMCastMemberRepository
from src.core.castmember.domain.castmember import CastMember


dotenv.load_dotenv()

@pytest.fixture
def admin_jwt_token():
    raw_private_key = os.getenv("AUTH_TEST_PRIVATE_KEY")
    private_key = f"-----BEGIN PRIVATE KEY-----\n{raw_private_key}\n-----END PRIVATE KEY-----"
    payload = {
        "aud": "account",
        "realm_access": {
            "roles": [
                "offline_access",
                "admin",
                "uma_authorization",
                "default-roles-codeflix"
            ]
        },
        
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1),
        "iat": datetime.datetime.now(datetime.UTC) ,
    }
    
    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token
    
@pytest.fixture
def auth_api_client(admin_jwt_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_jwt_token}")
    return client

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
        castmember_repository: DjangoORMCastMemberRepository,
        auth_api_client
        
    ) -> None:
        
        castmember_repository.save(actor_castmember)
        castmember_repository.save(director_castmember)
        

        url = "/api/cast_members/"
        response = auth_api_client.get(url)

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
        castmember_repository: DjangoORMCastMemberRepository,
        auth_api_client
        
    ) -> None:
        

        url = "/api/cast_members/"

        data = {
            "name": "Ana",
            "type": 'ACTOR'
        }
        response = auth_api_client.post(url, data)
        
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
        castmember_repository: DjangoORMCastMemberRepository,
        auth_api_client
    ) -> None:

        url = "/api/cast_members/"
        data = {
            "name": "Bruna",
            "type": 'Diretora'
        }
        response = auth_api_client.post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_create_castmember_invalid_name_return_400(
        self,
        castmember_repository: DjangoORMCastMemberRepository,
        auth_api_client
    ) -> None:

        url = "/api/cast_members/"
        data = {
            "name": "",
            "type": 'ACTOR'
        }
        response = auth_api_client.post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestDeleteAPI:
    def test_delete_non_existent_castmember_raise_404(
        self,
        auth_api_client
    ):
        url = f"/api/cast_members/{uuid4()}/"
        response = auth_api_client.delete(url)
        
        assert response.status_code == 404
    
    def test_delete_existent_genre(
        self,
        director_castmember: CastMember,
        castmember_repository: DjangoORMCastMemberRepository,
        auth_api_client
    ):
        
        castmember_repository.save(director_castmember)
        
        url = f"/api/cast_members/{director_castmember.id}/"
        response = auth_api_client.delete(url)
        
        assert response.status_code == 204
        
    def test_delete_invalid_pk(
        self,
        auth_api_client
    ):
        
        url = "/api/cast_members/ivalid-pk/"
        response = auth_api_client.delete(url)
        
        
        assert response.status_code == 400

@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_request_data_is_valid_then_update_castmember(
        self,
        actor_castmember: CastMember,
        director_castmember: CastMember,
        castmember_repository: DjangoORMCastMemberRepository,
        auth_api_client
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
        response = auth_api_client.put(url, data=data)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        updated_castmember = castmember_repository.get_by_id(actor_castmember.id)
        assert updated_castmember.name == 'Reinaldo 2'
        assert updated_castmember.type == 'DIRECTOR'
    
    def test_when_request_data_is_invalid_then_return_400(
        self,
        director_castmember: CastMember,
        castmember_repository: DjangoORMCastMemberRepository,
        auth_api_client
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
        response = auth_api_client.put(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"name": ["This field may not be blank."]}

    def test_when_type_do_not_exist_then_return_400(
        self,
        actor_castmember: CastMember,
        castmember_repository: DjangoORMCastMemberRepository,
        auth_api_client
    ) -> None:
        castmember_repository.save(actor_castmember)

        url = f"/api/cast_members/{str(actor_castmember.id)}/"
        data = {
            "name": "Reinaldo 1",
            "type": 'Ator'
        }
        response = auth_api_client.put(url, data=data)

        print(response.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_when_castmember_does_not_exist_then_return_404(self, auth_api_client) -> None:
        url = f"/api/cast_members/{str(uuid4())}/"
        data = {
            "name": "Diego",
            "type": 'ACTOR',
        }
        response = auth_api_client.put(url, data=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        
         