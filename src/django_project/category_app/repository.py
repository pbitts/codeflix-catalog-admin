


from uuid import UUID
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.django_project.category_app.models import Category as CategoryModel


class DjangoORMCategoryRepository(CategoryRepository):
    def __init__(self, category_model: CategoryModel = CategoryModel):
        self.category_model = category_model
        
    def save(self, category: Category) -> None:
        category_orm = CategoryModelMapper.to_model(category)
        category_orm.save()
        # self.category_model.objects.create(
        #     id=category.id,
        #     name=category.name,
        #     description=category.description,
        #     is_active=category.is_active
        # )
    
    def get_by_id(self, id: UUID) -> Category | None:
        try:
            category_model = self.category_model.objects.get(id=id)
            return CategoryModelMapper.to_entity(category_model)
            # return Category(
            #     id=category.id,
            #     name=category.name,
            #     description=category.description,
            #     is_active=category.is_active
            # )
        except self.category_model.DoesNotExist:
            return None
        
    def delete(self, id: UUID) -> None:
        self.category_model.objects.filter(id=id).delete()
    
    def list(self) -> list[Category]:
        return [
            CategoryModelMapper.to_entity(category_model)
            for category_model in self.category_model.objects.all()
        ]
        #  return [
        #      Category(
        #          id=category.id,
        #          name=category.name,
        #          description=category.description,
        #          is_active=category.is_active
        #      )
        #      for category in self.category_model.objects.all()
        #  ]
    
    def update(self, category: Category) -> None:
        self.category_model.objects.filter(pk=category.id).update(
            name=category.name,
            description=category.description,
            is_active=category.is_active
        )

class CategoryModelMapper:
    @staticmethod
    def to_model(category: Category) -> CategoryModel:
        return CategoryModel(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active
        )
    
    @staticmethod
    def to_entity(category_orm: CategoryModel) -> Category:
            return Category(
                id=category_orm.id,
                name=category_orm.name,
                description=category_orm.description,
                is_active=category_orm.is_active
            )