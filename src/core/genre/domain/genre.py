from dataclasses import dataclass, field
import uuid

from src.core._shared.entity import Entity


@dataclass
class Genre(Entity):
    name: str
    is_active: bool = True
    categories: set[uuid.UUID] = field(default_factory=set)
    
    
    def __post_init__(self):
        self.validate()
    
    def validate(self):
        if len(self.name) > 255:
            # raise ValueError("name cannot be longer than 255")
            self.notification.add_error("name cannot be longer than 255")

        if not self.name:
            # raise ValueError("name cannot be empty")
            self.notification.add_error("name cannot be empty")
        
        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def __str__(self):
        return f"Genre(name={self.name} (is_active={self.is_active}))"

    def __repr__(self):
        return self.__str__()

    def change_name(self, name = None):
        self.name = name
        self.validate()

    def activate(self):
        self.is_active = True
        self.validate()

    def deactivate(self):
        self.is_active = False
        self.validate()
        
    def add_category(self, category_id: uuid.UUID):
        self.categories.add(category_id)
        self.validate()
    
    def remove_category(self, category_id: uuid.UUID):
        self.categories.remove(category_id)
        self.validate()
        
    def update_categories(self, categories: set[uuid.UUID]):
        self.categories = categories
        self.validate()
    
