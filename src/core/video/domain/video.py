from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.core.video.domain.value_objects import Rating
from src.core._shared.entity import Entity


@dataclass
class Video(Entity):
    title: str
    description: str
    launch_year: int
    duration: Decimal
    published: bool
    rating: Rating
    
    categories: set[UUID]
    genres: set[UUID]
    cast_members: set[UUID]
    
    # TODO: adicionar atributos de midia
    
    def __post_init__(self):
        self.validate()
        
    def validate(self):
        if len(self.title) > 255:
            self.notification.add_error("title cannot be longer than 255")
        
        if not self.title:
            self.notification.add_error("title cannot be empty")
            
        if self.notification.has_errors:
            raise ValueError(self.notification.messages)
        
        
        