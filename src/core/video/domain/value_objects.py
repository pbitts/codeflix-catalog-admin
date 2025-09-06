from dataclasses import dataclass
from enum import Enum, auto, unique
from uuid import UUID


@unique # avoid repeating
class MediaStatus(Enum):
    PENDING = auto() # auto create value ex: 1, 2....
    PROCESSING = auto()
    COMPLETED = auto()
    ERROR = auto()
    

@unique
class Rating(Enum):
    ER = auto()
    L = auto()
    AGE_10 = auto() 
    AGE_12 = auto() 
    AGE_14 = auto() 
    AGE_16 = auto() 
    AGE_18 = auto()    
    
    
@dataclass(frozen=True)
class ImageMedia:
    id: UUID
    check_sum: str
    name: str
    location: str
    
    # Uses __eq__ standard from Python
    
    
@dataclass
class AudioVideoMedia:
    id: UUID
    check_sum: str
    name: str
    raw_location: str
    encoded_location: str
    status: MediaStatus