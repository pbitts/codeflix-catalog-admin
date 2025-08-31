from dataclasses import dataclass, field
from enum import StrEnum
import uuid

from src.core._shared.entity import Entity


class CastMemberType(StrEnum):
    ACTOR = "ACTOR"
    DIRECTOR = "DIRECTOR"
    
    
@dataclass
class CastMember(Entity):
    name: str
    type: CastMemberType
    
    def __post_init__(self):
        self.validate()
    
    def validate(self):
        if len(self.name) > 255:
            # raise ValueError("name cannot be longer than 255")
            self.notification.add_error("name cannot be longer than 255")

        if not self.name:
            # raise ValueError("name cannot be empty")
            self.notification.add_error("name cannot be empty")
        
        if self.type not in[CastMemberType.ACTOR, CastMemberType.DIRECTOR]:
            # raise ValueError("Type must be either 'ACTOR' or 'DIRECTOR'")
            self.notification.add_error("Type must be either 'ACTOR' or 'DIRECTOR'")
        
        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def __str__(self):
        return f"CastMember(name={self.name} (type={self.type}))"

    def __repr__(self):
        return self.__str__()

    def change_name(self, name = None):
        self.name = name
        self.validate()
        
    def update_type(self, type: CastMemberType):
        self.type = type
        self.validate()
    
