import uuid
from django.utils import timezone
from django.db import models
from datetime import date
from .users import CustomUser
from .groups import Group

class Feed(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=5000)
    img = models.ImageField(upload_to="uploads/feeds", blank=True)
    isPublic = models.BooleanField(default=True)
    isDeleted = models.BooleanField(default=False)
    createdBy = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)
    belongTo = models.ForeignKey("Group", on_delete=models.CASCADE, null=True, blank=True)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)