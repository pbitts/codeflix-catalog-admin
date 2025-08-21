from dataclasses import dataclass, field
import uuid

@dataclass
class Category:
    name: str
    description: str = ""
    is_active: bool = True
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    
    def __post_init__(self):
        self.validate()
    
    def validate(self):
        if len(self.name) > 255:
            raise ValueError("name cannot be longer than 255")

        if not self.name:
            raise ValueError("name cannot be empty")

    def __str__(self):
        return f"Category(name={self.name} - description={self.description} (is_active={self.is_active}))"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Category):
            return False
        return self.id == other.id

    def update_category(self, name = None, description = None):
        if name:
            self.name = name
        if description:
            self.description = description

        self.validate()

    def activate(self):
        self.is_active = True
        self.validate()

    def deactivate(self):
        self.is_active = False
        self.validate()
    
