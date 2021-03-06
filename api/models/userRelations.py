from django.db import models
from django.utils import timezone

#Book like/dislike by user
class UserBook(models.Model):
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
class UserMovie(models.Model):
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

#Feed like/dislike by user
class UserFeed(models.Model):
    CHOICE=(
        ('O', 'Other'),
        ('L', 'Like'),
        ('D', 'Dislike'),
    )
    feed = models.ForeignKey("Feed", on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)
    response = models.CharField(choices=CHOICE, max_length=10, null=False, blank=False,default='O')
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('feed','user')

#Review like/dislike by user
class UserReview(models.Model):
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

    class Meta:
        unique_together = ('review','user')

#Group joined by user
class UserGroup(models.Model):
    group = models.ForeignKey("Group", on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)
    isAdmin = models.BooleanField(default=False)
    isMainAdmin = models.BooleanField(default=False)
    isBanned = models.BooleanField(default=False)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)
    banDue = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('group','user')

#Tag joined by user
class UserTag(models.Model):
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)
    #isJoined = models.BooleanField(default=False)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('tag','user')