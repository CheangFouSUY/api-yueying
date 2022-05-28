import uuid
from django.db import models

class Feedback(models.Model):
    CATEGORY = (
        (1, 'BUG反馈'),
        (2, '网站反馈'),
        (3, '其它'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=5000)
    category = models.IntegerField(choices=CATEGORY, default=1)
    createdBy = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)
