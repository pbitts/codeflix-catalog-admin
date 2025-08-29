from uuid import UUID
from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response

from src.core.castmember.application.use_cases.delete_castmember import DeleteCastMember
from src.core.castmember.application.use_cases.update_castmember import UpdateCastMember
from src.core.castmember.application.exceptions import CastMemberNotFound, InvalidCastMember, InvalidCastMemberType
from src.core.castmember.application.use_cases.create_castmember import CreateCastMember
from src.django_project.castmember_app.serializers import CreateCastMemberInputSerializer, CreateCastMemberOutputSerializer, DeleteCastMemberInputSerializer, ListCastMemberOutputSerializer, UpdateCastMemberInputSerializer
from src.django_project.castmember_app.repository import DjangoORMCastMemberRepository
from src.core.castmember.application.use_cases.list_castmember import ListCastMember


class CastMemberViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        use_case = ListCastMember(repository=DjangoORMCastMemberRepository())
        output: ListCastMember.Output = use_case.execute(ListCastMember.Input())
        response_serializer = ListCastMemberOutputSerializer(output)
        
        return Response(data=response_serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request) -> Response:
        serializer = CreateCastMemberInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        input = CreateCastMember.Input(**serializer.validated_data)
        use_case = CreateCastMember(
            repository=DjangoORMCastMemberRepository()
            )
        try:
            output = use_case.execute(input)
        except (InvalidCastMember, InvalidCastMemberType) as err:
            return Response(data={"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data=CreateCastMemberOutputSerializer(output).data, status=status.HTTP_201_CREATED)

    def destroy(self, request: Request, pk: UUID = None):
        request_data = DeleteCastMemberInputSerializer(data={"id": pk})
        request_data.is_valid(raise_exception=True)
        
        input = DeleteCastMember.Input(**request_data.validated_data)
        use_case = DeleteCastMember(repository=DjangoORMCastMemberRepository())
        try:
            use_case.execute(input)
        except CastMemberNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request: Request, pk: str = None) -> Response:
        serializer = UpdateCastMemberInputSerializer(
            data = {
                **request.data,
                "id": pk
            }
        )
        serializer.is_valid(raise_exception=True)
        
        input = UpdateCastMember.Input(**serializer.validated_data)
        use_case = UpdateCastMember(
            repository=DjangoORMCastMemberRepository()
        )
        
        try:
            use_case.execute(input)
        except (InvalidCastMemberType, InvalidCastMember) as err:
            return Response(data={"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except CastMemberNotFound as err:
            return Response(data={"error": str(err)}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(status=status.HTTP_204_NO_CONTENT)


