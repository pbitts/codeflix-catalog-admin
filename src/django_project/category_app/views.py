from uuid import UUID
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_200_OK, 
    HTTP_400_BAD_REQUEST, 
    HTTP_404_NOT_FOUND, 
    HTTP_201_CREATED
)

from src.core.category.application.use_cases.create_category import CreateCategory, CreateCategoryRequest
from django_project.category_app.serializers import CategoryResponseSerializer, CreateCategoryRequestSerializer, CreateCategoryResponseSerializer, ListCategoryResponseSerializer, RetrieveCategoryRequestSerializer, RetrieveCategoryResponseSerializer
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest
from src.core.category.application.use_cases.list_category import (
    ListCategory, 
    ListCategoryRequest,
    ListCategoryResponse
)
from django_project.category_app.repository import DjangoORMCategoryRepository

class CategoryViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving categories.
    """
    
    def list(self, request: Request) -> Response:
        
        input = ListCategoryRequest()
        use_case = ListCategory(repository=DjangoORMCategoryRepository())
        response = use_case.execute(input)
        
        serializer = ListCategoryResponseSerializer(instance=response)
        
        return Response(status=HTTP_200_OK, data=serializer.data)
    
    def retrieve(self, request: Request, pk: str = None) -> Response:
        
        serializer = RetrieveCategoryRequestSerializer(data={'id': pk})
        serializer.is_valid(raise_exception=True)
        
        use_case = GetCategory(repository=DjangoORMCategoryRepository())
        
        try:
            result = use_case.execute(GetCategoryRequest(id=serializer.validated_data['id']))
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        
        category_output = RetrieveCategoryResponseSerializer(instance=result)
        
        return Response(status=HTTP_200_OK, data=category_output.data)
    
    def create(self, request: Request) -> Response:
        
        serializer = CreateCategoryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        input = CreateCategoryRequest(**serializer.validated_data)
        use_case = CreateCategory(repository=DjangoORMCategoryRepository())
        output = use_case.execute(request=input)
        
        return Response(
            status=HTTP_201_CREATED,
            data=CreateCategoryResponseSerializer(instance=output).data
        )