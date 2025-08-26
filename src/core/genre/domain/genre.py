from dataclasses import dataclass, field
import uuid

@dataclass
class Genre:
    name: str
    is_active: bool = True
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    categories: set[uuid.UUID] = field(default_factory=set)
    
    def __post_init__(self):
        self.validate()
    
    def validate(self):
        if len(self.name) > 255:
            raise ValueError("name cannot be longer than 255")

        if not self.name:
            raise ValueError("name cannot be empty")

    def __str__(self):
        return f"Genre(name={self.name} (is_active={self.is_active}))"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Genre):
            return False
        return self.id == other.id

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
    
