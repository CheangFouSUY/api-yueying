import uuid
from django.utils import timezone
from django.db import models
from datetime import date

class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    isbn = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=5000)
    img = models.ImageField(upload_to="uploads/books", blank=True)
    thumbnail = models.ImageField(upload_to="uploads/books", blank=True)
    author = models.CharField(max_length=150)
    publisher = models.CharField(max_length=150)
    year = models.DateField(default=date(2000, 1, 1))
    category = models.CharField(max_length=150)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)