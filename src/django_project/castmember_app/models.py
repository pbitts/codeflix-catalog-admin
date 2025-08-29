from uuid import uuid4
from django.db import models

class CastMember(models.Model):
    app_label = 'castmember_app'
    
    class CastMemberType(models.TextChoices):
        ACTOR = 'ACTOR', 'ACTOR'
        DIRECTOR = 'DIRECTOR', 'DIRECTOR'
    
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=CastMemberType.choices)
    
    class Meta:
        db_table = "castmember"
        
    def __str__(self):
        return self.name
