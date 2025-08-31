
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.category.application.use_cases.list_category import CategoryOutput, ListCategory, ListCategoryRequest, ListCategoryResponse
from src.core.category.domain.category import Category


class TestListCategory:
    def test_return_empty_list(self):
        
        category = Category(name="Movie", description="some description")
        repository = InMemoryCategoryRepository(categories=[])
        use_case = ListCategory(repository=repository)
        request = ListCategoryRequest()
        response = use_case.execute(request)
        
        assert response == ListCategoryResponse(data=[])
    
    def test_return_list_of_categories(self):
        
        category1 = Category(name="Movie", description="some description")
        category2 = Category(name="Documentary", description="some description")
        repository = InMemoryCategoryRepository(categories=[])
        repository.save(category1)
        repository.save(category2)
        use_case = ListCategory(repository=repository)
        request = ListCategoryRequest()
        response = use_case.execute(request)
        
        assert response == ListCategoryResponse(
            data=[
                CategoryOutput(
                    id=category2.id,
                    name=category2.name,
                    description=category2.description,
                    is_active=category2.is_active
                ),
                CategoryOutput(
                    id=category1.id,
                    name=category1.name,
                    description=category1.description,
                    is_active=category1.is_active
                )
                
            ]
        )