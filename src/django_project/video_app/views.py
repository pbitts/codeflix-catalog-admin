from uuid import UUID
from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response

from src.core.video.application.exceptions import RelatedEntitiesNotFound
from src.core.video.application.use_cases.create_video_without_media import CreateVideoWithoutMedia
from src.django_project.castmember_app.repository import DjangoORMCastMemberRepository
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.video_app.serializers import CreateVideoInputSerializer, CreateVideoOutputSerializer
from src.django_project.video_app.repository import DjangoORMVideoRepository

class VideoViewSet(viewsets.ViewSet):
    def create(self, request: Request) -> Response:
        serializer = CreateVideoInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        input = CreateVideoWithoutMedia.Input(**serializer.validated_data)
        use_case = CreateVideoWithoutMedia(
            video_repository=DjangoORMVideoRepository(),
            category_repository=DjangoORMCategoryRepository(),
            genre_repository=DjangoORMGenreRepository(),
            castmember_repository=DjangoORMCastMemberRepository()
            )
        try:
            output = use_case.execute(input)
        except (RelatedEntitiesNotFound) as err:
            return Response(data={"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data=CreateVideoOutputSerializer(output).data, status=status.HTTP_201_CREATED)