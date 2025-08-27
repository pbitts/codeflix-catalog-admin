from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response

from src.core.genre.application.use_cases.list_genre import ListGenre
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.serializers import ListGenreOutputSerializer


class GenreViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        use_case = ListGenre(repository=DjangoORMGenreRepository())
        output: ListGenre.Output = use_case.execute(ListGenre.Input())
        response_serializer = ListGenreOutputSerializer(output)
        
        return Response(data=response_serializer.data, status=status.HTTP_200_OK)