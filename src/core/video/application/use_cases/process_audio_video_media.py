from dataclasses import dataclass
from uuid import UUID

from src.core.video.application.exceptions import MediaNotFound, VideoNotFound
from src.core.video.domain.value_objects import MediaStatus, MediaType
from src.core.video.domain.video_repository import VideoRepository


class ProcessAudioVideoMedia:
    
    @dataclass
    class Input:
        encoded_location: str
        video_id: UUID
        status: MediaStatus
        media_type: MediaType
        
    def __init__(self, video_repository: VideoRepository):
        self.video_repository = video_repository
    
    def execute(self, input: Input):
        video = self.video_repository.get_by_id(id=input.video_id)
        if video is None:
            raise VideoNotFound(f"Video with id {input.video_id} not found")
        
        if input.media_type == MediaType.VIDEO:
            if not video.video:
                raise MediaNotFound("Video must have media to be processed")
            
            video.process(status=input.status, encoded_location=input.encoded_location)
        
        self.video_repository.update(video)