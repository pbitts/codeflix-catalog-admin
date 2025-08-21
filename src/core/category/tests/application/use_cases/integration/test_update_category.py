from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestUpdateCategory:
    def test_update_category_name_and_description(self):
        category = Category( name="Movie", description="some description")
        
        repository = InMemoryCategoryRepository()
        repository.save(category)
        
        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=category.id,
            name="Updated Movie",
            description="Updated description"
        )
        
        use_case.execute(request)
        
        update_category = repository.get_by_id(category.id)
        assert update_category.name == "Updated Movie"
        assert update_category.description == "Updated description"