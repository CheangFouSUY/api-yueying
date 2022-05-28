import uuid
from django.utils import timezone
from django.db import models
from ..utils import get_thumbnail

class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=5000)
    img = models.ImageField(upload_to="uploads/reviews", blank=True)
    isDeleted = models.BooleanField(default=False)
    createdBy = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)
    feed = models.ForeignKey("Feed", on_delete=models.CASCADE, null=True, blank=True, default=None)
    book = models.ForeignKey("Book", on_delete=models.CASCADE, null=True, blank=True, default=None)
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE, null=True, blank=True, default=None)

    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self.img:
            self.img = get_thumbnail(self.img, 100, False)     # quality = 100, isThumbnail False = maxWidthHeight = 1024px
        super(Review, self).save(*args, **kwargs)