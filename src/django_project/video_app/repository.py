from uuid import UUID
from django.db import transaction

from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository
from src.django_project.video_app.models import Video as VideoModel

class DjangoORMVideoRepository(VideoRepository):
    
    def save(self, video: Video):
        video_model = VideoModelMapper.to_model(video)
        with transaction.atomic():
            video_model.save()
            
            
            video_model.categories.set(video.categories)
            video_model.genres.set(video.genres)
            video_model.cast_members.set(video.cast_members)
            
    
    def get_by_id(self, id: UUID) -> Video:
        try:
            video_model = VideoModel.objects.get(id=id)
            return VideoModelMapper.to_entity(video_model)
        except VideoModel.DoesNotExist:
            return None

    
    def list(self) -> list[Video]:
        return [
            VideoModelMapper.to_entity(video_model)
            for video_model in VideoModel.objects.all()
        ]
    
    def update(self):
        pass
    
    def delete(self):
        pass
 
    

class VideoModelMapper:
    @staticmethod
    def to_model(video: Video) -> VideoModel:
        """Converte entidade de domínio para modelo ORM (sem salvar categorias)."""
        return VideoModel(
            title=video.title,
            description=video.description,
            launch_year=video.launch_year,
            published=False,
            opened=video.opened,
            duration=video.duration,
            rating=video.rating,
        )

    @staticmethod
    def to_entity(video_model: VideoModel) -> Video:
        """Converte modelo ORM para entidade de domínio."""
        return Video(
            id=video_model.id,
            title=video_model.title,
            description=video_model.description,
            launch_year=video_model.launch_year,
            opened=video_model.opened,
            duration=video_model.duration,
            rating=video_model.rating,
            published=video_model.published,
            categories=set(video_model.categories.values_list("id", flat=True)),
            genres=set(video_model.genres.values_list("id", flat=True)),
            cast_members=set(video_model.cast_members.values_list("id", flat=True)),
        )