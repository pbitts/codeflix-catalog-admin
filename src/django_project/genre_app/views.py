from uuid import UUID
from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response

from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.core.genre.application.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.application.use_cases.list_genre import ListGenre
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.serializers import CreateGenreInputSerializer, CreateGenreOutputSerializer, DeleteGenreInputSerializer, ListGenreOutputSerializer, UpdateGenreInputSerializer


class GenreViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        use_case = ListGenre(repository=DjangoORMGenreRepository())
        output: ListGenre.Output = use_case.execute(ListGenre.Input())
        response_serializer = ListGenreOutputSerializer(output)
        
        return Response(data=response_serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request: Request) -> Response:
        serializer = CreateGenreInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        input = CreateGenre.Input(**serializer.validated_data)
        use_case = CreateGenre(
            repository=DjangoORMGenreRepository(),
            category_repository=DjangoORMCategoryRepository()
            )
        try:
            output = use_case.execute(input)
        except (InvalidGenre, RelatedCategoriesNotFound) as err:
            return Response(data={"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data=CreateGenreOutputSerializer(output).data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request: Request, pk: UUID = None):
        request_data = DeleteGenreInputSerializer(data={"id": pk})
        request_data.is_valid(raise_exception=True)
        
        input = DeleteGenre.Input(**request_data.validated_data)
        use_case = DeleteGenre(repository=DjangoORMGenreRepository())
        try:
            use_case.execute(input)
        except GenreNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request: Request, pk: str = None) -> Response:
        serializer = UpdateGenreInputSerializer(
            data = {
                **request.data,
                "id": pk
            }
        )
        serializer.is_valid(raise_exception=True)
        
        input = UpdateGenre.Input(**serializer.validated_data)
        use_case = UpdateGenre(
            repository=DjangoORMGenreRepository(),
            category_repository=DjangoORMCategoryRepository())
        
        try:
            use_case.execute(input)
        except (RelatedCategoriesNotFound, InvalidGenre) as err:
            return Response(data={"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except GenreNotFound as err:
            return Response(data={"error": str(err)}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(status=status.HTTP_204_NO_CONTENT)

