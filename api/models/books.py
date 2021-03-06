import uuid
from django.utils import timezone
from django.db import models
from datetime import date
from ..utils import get_thumbnail

class Book(models.Model):
    CATEGORY = (
        (0, '其他'),
        (1, '爱情'),
        (2, '恐怖'),
        (3, '悬疑'),
        (4, '科幻'),
        (5, '艺术'),
        (6, '体育'),
        (7, '烹饪'),
        (8, '漫画'),
        (9, '教育'),
        (10, '哲学'),
        (11, '文学'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    isbn = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=5000)
    img = models.ImageField(upload_to="uploads/books", blank=True)
    thumbnail = models.ImageField(upload_to="uploads/books", blank=True)
    author = models.CharField(max_length=150)
    publisher = models.CharField(max_length=150)
    year = models.DateField(default=date(2000, 1, 1))
    category = models.IntegerField(choices=CATEGORY,null=False, blank=False,default=0)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self.img:
            # ratio 3:4 0.75
            self.img = get_thumbnail(self.img, 100, False, 0.75)     # quality = 100, isThumbnail False = maxWidthHeight = 1024px
            self.thumbnail = get_thumbnail(self.img, 100, True, 0.75)    # quality = 100, isThumbnail False = maxWidthHeight = 256px
        super(Book, self).save(*args, **kwargs)