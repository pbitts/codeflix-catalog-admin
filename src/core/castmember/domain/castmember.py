from dataclasses import dataclass, field
from enum import StrEnum
import uuid


class CastMemberType(StrEnum):
    ACTOR = "ACTOR"
    DIRECTOR = "DIRECTOR"
    
    
@dataclass
class CastMember:
    name: str
    type: CastMemberType
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    
    def __post_init__(self):
        self.validate()
    
    def validate(self):
        if len(self.name) > 255:
            raise ValueError("name cannot be longer than 255")

        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("name cannot be empty")
        
        if self.type not in[CastMemberType.ACTOR, CastMemberType.DIRECTOR]:
            raise ValueError("Type must be either 'ACTOR' or 'DIRECTOR'")

    def __str__(self):
        return f"CastMember(name={self.name} (type={self.type}))"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, CastMember):
            return False
        return self.id == other.id

    def change_name(self, name = None):
        self.name = name
        self.validate()
        
    def update_type(self, type: CastMemberType):
        self.type = type
        self.validate()
    
