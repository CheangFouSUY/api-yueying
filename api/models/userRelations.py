from django.db import models
from django.utils import timezone

#Book like/dislike by user
class userBook(models.Model):
    CHOICE=(
        ('O', 'Other'),
        ('L', 'Like'),
        ('D', 'Dislike'),
    )
    book = models.ForeignKey("Book", on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)
    response = models.CharField(choices=CHOICE, max_length=10, null=False, blank=False,default='O')
    isSaved = models.BooleanField(default=False)
    isRated = models.BooleanField(default=False)
    rateScore = models.IntegerField(default=-1)     # socre effective when > 0
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)

#Movie like/dislike by user
class userMovie(models.Model):
    CHOICE=(
        ('O', 'Other'),
        ('L', 'Like'),
        ('D', 'Dislike'),
    )
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)
    response = models.CharField(choices=CHOICE, max_length=10, null=False, blank=False,default='O')
    isSaved = models.BooleanField(default=False)
    isRated = models.BooleanField(default=False)
    rateScore = models.IntegerField(default=-1)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)

#Feed followed,like/dislike by user
class userFeed(models.Model):
    CHOICE=(
        ('O', 'Other'),
        ('L', 'Like'),
        ('D', 'Dislike'),
    )
    feed = models.ForeignKey("Feed", on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)
    response = models.CharField(choices=CHOICE, max_length=10, null=False, blank=False,default='O')
    isFollowed = models.BooleanField(default=False)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)

#Review like/dislike by user
class userReview(models.Model):
    CHOICE=(
        ('O', 'Other'),
        ('L', 'Like'),
        ('D', 'Dislike'),
    )
    review = models.ForeignKey("Review", on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)
    response = models.CharField(choices=CHOICE, max_length=10, null=False, blank=False,default='O')
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)

#Group joined by user
class userGroup(models.Model):
    group = models.ForeignKey("Group", on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)
    isAdmin = models.BooleanField(default=False)
    isBanned = models.BooleanField(default=False)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)

