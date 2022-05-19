from django.db import models
from django.utils import timezone

#Feed belong to a group
class GroupFeed(models.Model):
    feed = models.OneToOneField("Feed", on_delete=models.CASCADE, null=False, blank=False)
    group = models.ForeignKey("Group", on_delete=models.CASCADE, null=False, blank=False)
    isPin = models.BooleanField(default=False)
    isFeatured = models.BooleanField(default=False)
    #isNormal = models.BooleanField(default=True)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)

class GroupAdminRequest(models.Model):
    RESULT = (
        (0, 'Pending'),
        (1, 'Accept'),
        (2, 'Decline'),
    )
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)
    group = models.ForeignKey("Group", on_delete=models.CASCADE, null=False, blank=False)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)
    result = models.IntegerField(choices=RESULT,null=False, blank=False, default=0)
