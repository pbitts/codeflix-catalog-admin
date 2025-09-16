from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID

from src.core.video.domain.value_objects import AudioVideoMedia, ImageMedia, MediaStatus, MediaType, Rating
from src.core._shared.entity import Entity


@dataclass
class Video(Entity):
    title: str
    description: str
    launch_year: int
    duration: Decimal
    opened: bool
    rating: Rating
    
    
    categories: set[UUID]
    genres: set[UUID]
    cast_members: set[UUID]
    
    published: bool = field(default=False)
    
    banner: ImageMedia | None = None
    thumbnail: ImageMedia | None = None
    thumbnail_half: ImageMedia | None = None
    trailer: AudioVideoMedia | None = None
    video: AudioVideoMedia | None = None
    
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
    
    def publish(self) -> None:
        if not self.video:
            self.notification.add_error("Video media is required to publish the video")
        elif self.video.status != MediaStatus.COMPLETED:
            self.notification.add_error("Video must be fully processed to be published")

        self.published = True
        self.validate()
    
    def update(self, title, desciption, launch_year, duration, published, rating):
        self.title = title
        self.desciption = desciption
        self.launch_year = launch_year
        self.duration = duration
        self.published = published
        self.rating = rating
    
        self.validate()
        
    def add_category(self, category_id: UUID) -> None:
        self.categories.add(category_id)
        self.validate()
    
    def add_genre(self, genre_id: UUID) -> None:
        self.genres.add(genre_id)
        self.validate()
    
    def add_cast_members(self, cast_members_id: UUID) -> None:
        self.cast_members.add(cast_members_id)
        self.validate()
    
    def update_banner(self, banner: ImageMedia) -> None:
        self.banner = banner
        self.validate()

    def update_thumbnail(self, thumbnail: ImageMedia) -> None:
        self.thumbnail = thumbnail
        self.validate()
        
    def update_thumbnail_half(self, thumbnail_half: ImageMedia) -> None:
        self.thumbnail_half = thumbnail_half
        self.validate()
    
    def update_trailer(self, trailer: AudioVideoMedia) -> None:
        self.trailer = trailer
        self.validate()
    
    def update_video_media(self, video: AudioVideoMedia) -> None:
        self.video = video
        self.validate()
        
    def process(self, status, encoded_location):
        if status == MediaStatus.COMPLETED:
            self.video = AudioVideoMedia(
                name=self.video.name,
                raw_location=self.video.raw_location,
                media_type=MediaType.VIDEO,
                encoded_location=encoded_location,
                status=MediaStatus.COMPLETED
            )
            self.publish()
        else:
            self.video = AudioVideoMedia(
                name=self.video.name,
                raw_location=self.video.raw_location,
                media_type=MediaType.VIDEO,
                encoded_location="",
                status=MediaStatus.ERROR
            )
        
        self.validate()
        
    
    
        
        
        