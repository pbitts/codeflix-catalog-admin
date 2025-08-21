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
    
    def delete(self, id: UUID) -> None:
        Category = self.get_by_id(id)
        self.categories.remove(Category)
    
    def update(self, category: Category) -> None:
        old_category = self.get_by_id(category.id) 
        if old_category:
            self.categories.remove(old_category)
            self.categories.append(category)
    
    def list(self) -> list[Category]:
        # Return a copy of the categories list to avoid external modifications
        return [category for category in self.categories]