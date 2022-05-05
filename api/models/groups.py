import uuid
from django.utils import timezone
from django.db import models
from datetime import date
from .users import CustomUser

class Group(models.Model):
    CATEGORIES = (
        ("b", "Book"),
        ("m", "Movie"),
        ("o", "Other"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    groupName = models.CharField(max_length=150)
    description = models.TextField(max_length=5000)
    category = models.CharField(max_length=150, choices=CATEGORIES, default=CATEGORIES[0][0])
    createdBy = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)
    isDeleted = models.BooleanField(default=False)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)