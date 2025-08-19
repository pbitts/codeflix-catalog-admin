import uuid


class Category:
    def __init__(self, name, id = "", description = "", is_active = True):
        self.name = name
        self.id = id or uuid.uuid4()
        self.description = description
        self.is_active = is_active

        if len(self.name) > 255:
            raise ValueError("name must be less than 256 characters")
    
    def __str__(self):
        return f"Category(name={self.name} - description={self.description} (is_active={self.is_active}))"

    def __repr__(self):
        return self.__str__()