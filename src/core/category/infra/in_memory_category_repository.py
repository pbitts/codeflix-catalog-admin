from uuid import UUID

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.domain.category import Category


class InMemoryCategoryRepository(CategoryRepository):
    def __init__(self, categories=None):
        self.categories = categories or []
    
    def save(self, category):
        self.categories.append(category)
    
    def get_by_id(self, id: UUID) -> Category | None:
        return next((Category for Category in self.categories if Category.id == id), None)