import uuid
from django.utils import timezone
from django.db import models
from datetime import date


class Movie(models.Model):
    CATEGORY = (
        (0, '其他'),
        (1, '爱情'),
        (2, '恐怖'),
        (3, '悬疑'),
        (4, '冒险'),
        (5, '喜剧'),
        (6, '动作'),
        (7, '科幻'),
        (8, '综艺'),
        (9, '动漫'),
        (10, '卡通'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=5000)
    img = models.ImageField(upload_to="uploads/movies", blank=True)
    thumbnail = models.ImageField(upload_to="uploads/movies", blank=True)
    director = models.CharField(max_length=150)
    actor = models.CharField(max_length=150)
    year = models.DateField(default=date(2000, 1, 1))
    category = models.IntegerField(choices=CATEGORY,null=False, blank=False,default=0)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)