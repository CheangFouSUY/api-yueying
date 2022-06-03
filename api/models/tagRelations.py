from django.db import models
from django.utils import timezone

#Feed belong to tag
class TagFeed(models.Model):
    feed = models.ForeignKey("Feed", on_delete=models.CASCADE, null=False, blank=False)
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE, null=False, blank=False)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)

