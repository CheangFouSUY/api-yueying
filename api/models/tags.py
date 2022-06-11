import uuid
from django.db import models
from django.utils import timezone

class Tag(models.Model):
    CATEGORY = (
        ('b', 'Book'),
        ('m', 'Movie'),
        ('o', 'Other'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    category = models.CharField(max_length=5,choices=CATEGORY, default='o')
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)
