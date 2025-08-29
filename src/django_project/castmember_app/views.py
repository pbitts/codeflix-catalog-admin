from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response

from src.django_project.castmember_app.serializers import ListCastMemberOutputSerializer
from src.django_project.castmember_app.repository import DjangoORMCastMemberRepository
from src.core.castmember.application.use_cases.list_castmember import ListCastMember


class CastMemberViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        use_case = ListCastMember(repository=DjangoORMCastMemberRepository())
        output: ListCastMember.Output = use_case.execute(ListCastMember.Input())
        response_serializer = ListCastMemberOutputSerializer(output)
        
        return Response(data=response_serializer.data, status=status.HTTP_200_OK)
