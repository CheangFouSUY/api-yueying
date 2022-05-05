from django.db import models
from django.utils import timezone

#Feed belong to a group
class groupFeed(models.Model):
    feed = models.ForeignKey("Feed", on_delete=models.CASCADE, null=False, blank=False)
    group = models.ForeignKey("Group", on_delete=models.CASCADE, null=False, blank=False)
    isPin = models.BooleanField(default=False)
    isFeatured = models.BooleanField(default=False)
    #isNormal = models.BooleanField(default=True)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)
