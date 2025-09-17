from dataclasses import dataclass
from enum import Enum, StrEnum, auto, unique
from uuid import UUID


@unique # avoid repeating
class MediaStatus(StrEnum):
    PENDING = "PENDING" 
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"
    

@unique
class Rating(StrEnum):
    ER = "ER"
    L = "L"
    AGE_10 = "AGE_10"
    AGE_12 = "AGE_12"
    AGE_14 = "AGE_14" 
    AGE_16 = "AGE_16"
    AGE_18 = "AGE_18"  
    
    
@dataclass(frozen=True)
class ImageMedia:
    check_sum: str
    name: str
    location: str
    
    # Uses __eq__ standard from Python
    
@unique
class MediaType(StrEnum):
    VIDEO = "VIDEO"
    TRAILER = "TRAILER"
    BANNER = "BANNER"
    THUMBNAIL = "THUMBNAIL"
    THUMBNAIL_HALF = "THUMBNAIL_HALF"
    
    
@dataclass
class AudioVideoMedia:
    name: str
    raw_location: str
    encoded_location: str
    status: MediaStatus
    media_type: MediaType

    
