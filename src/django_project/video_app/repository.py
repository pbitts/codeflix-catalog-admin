from uuid import UUID
from django.db import transaction

from src.core.video.domain.value_objects import AudioVideoMedia
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository
from src.django_project.video_app.models import AudioVideoMedia as AudioVideoMediaModel, Video as VideoModel

class DjangoORMVideoRepository(VideoRepository):
    
    def save(self, video: Video):
        
        with transaction.atomic():
            video_model = VideoModel.objects.create(
                title=video.title,
                description=video.description,
                launch_year=video.launch_year,
                opened=video.opened,
                duration=video.duration,
                rating=video.rating
            )
            
            video_model.categories.set(video.categories)
            video_model.genres.set(video.genres)
            video_model.cast_members.set(video.cast_members)
            
    
    def get_by_id(self, id: UUID) -> Video | None:
        try:
            video_model = VideoModel.objects.get(id=id)
        except VideoModel.DoesNotExist:
            return None
        else:
            return VideoModelMapper.to_entity(video_model)

    
    def list(self) -> list[Video]:
        return [
            VideoModelMapper.to_entity(video_model)
            for video_model in VideoModel.objects.all()
        ]
    
    def update(self, video: Video) -> None:
        try:
            video_model = VideoModel.objects.get(pk=video.id)
        except VideoModel.DoesNotExist:
            return None
        else:
            AudioVideoMediaModel.objects.filter(id=video.id).delete()
            
            video_model.categories.set(video.categories)
            video_model.genres.set(video.genres)
            video_model.cast_members.set(video.cast_members)
            
            # persist value object
            video_model.video = AudioVideoMediaModel.objects.create(
                name=video.video.name,
                raw_location=video.video.raw_location,
                encoded_location=video.video.encoded_location,
                status=video.video.status
            )
            
            video_model.title = video.title
            video_model.description = video.description
            video_model.launch_year = video.launch_year
            video_model.opened = video.opened
            video_model.duration = video.duration
            video_model.rating = video.rating
            video_model.published = video.published
            
            video_model.save()
            
            
    
    def delete(self):
        VideoModel.objects.filter(pk=id).delete()
 
    

class VideoModelMapper:
    @staticmethod
    def to_model(video: Video) -> VideoModel:
        """Converte entidade de domínio para modelo ORM (sem salvar categorias)."""
        return VideoModel(
            title=video.title,
            description=video.description,
            launch_year=video.launch_year,
            opened=video.opened,
            duration=video.duration,
            rating=video.rating,
        )

    @staticmethod
    def to_entity(model: VideoModel) -> Video:
        video = Video(
            id=model.id,
            title=model.title,
            description=model.description,
            launch_year=model.launch_year,
            opened=model.opened,
            duration=model.duration,
            rating=model.rating,
            published=model.published,
            categories=set(model.categories.values_list("id", flat=True)),
            genres=set(model.genres.values_list("id", flat=True)),
            cast_members=set(model.cast_members.values_list("id", flat=True)),
        )

        if model.video:
            video.video = AudioVideoMedia(
                name=model.video.name,
                raw_location=model.video.raw_location,
                encoded_location=model.video.encoded_location,
                status=model.video.status
            )

        return video