import uuid
from django.utils import timezone
from django.db import models
from datetime import date
from .users import CustomUser
from ..utils import get_thumbnail

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
    img = models.ImageField(upload_to="uploads/groups", blank=True)
    thumbnail = models.ImageField(upload_to="uploads/groups", blank=True)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self.img:
            # ratio 1:1
            self.img = get_thumbnail(self.img, 100, False, 1)     # quality = 100, isThumbnail False = maxWidthHeight = 1024px
            self.thumbnail = get_thumbnail(self.img, 100, True, 1)    # quality = 100, isThumbnail False = maxWidthHeight = 256px
        super(Group, self).save(*args, **kwargs)