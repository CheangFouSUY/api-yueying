from django.contrib import admin

from .models.feedbacks import Feedback
from .models.reports import Report
from .models.users import CustomUser
from .models.books import Book
from .models.movies import Movie
from .models.groups import Group
from .models.feeds import Feed
from .models.reviews import Review
from .models.userRelations import *
from .models.groupRelations import *

# Register your models here.

class UserAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'profile')

class BookAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'isbn', 'title', 'year', 'img')

class MovieAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'title', 'year', 'img')

class GroupAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'groupName', 'category','createdBy')

class FeedAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'title', 'isPublic','createdBy', 'belongTo', 'img')

class ReviewAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'title', 'createdBy', 'img')

class ReportAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'title', 'category','createdBy','result')

class FeedbackAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'title', 'createdBy')

class UserBookAdminConfig(admin.ModelAdmin):
    list_display = ('book', 'user', 'response', 'isSaved')

class UserMovieAdminConfig(admin.ModelAdmin):
    list_display = ('movie', 'user', 'response', 'isSaved')

class UserFeedAdminConfig(admin.ModelAdmin):
    list_display = ('feed', 'user', 'response', 'isFollowed')

class UserReviewAdminConfig(admin.ModelAdmin):
    list_display = ('review', 'user', 'response')

class UserGroupAdminConfig(admin.ModelAdmin):
    list_display = ('group', 'user', 'isAdmin', 'isMainAdmin','isBanned')

class GroupFeedAdminConfig(admin.ModelAdmin):
    list_display = ('feed', 'group', 'isPin', 'isFeatured')

class GroupAdminApplyConfig(admin.ModelAdmin):
    list_display = ('user','group','result')


admin.site.register(CustomUser, UserAdminConfig)
admin.site.register(Book, BookAdminConfig)
admin.site.register(Movie, MovieAdminConfig)
admin.site.register(Group, GroupAdminConfig)
admin.site.register(Feed, FeedAdminConfig)
admin.site.register(Review, ReviewAdminConfig)
admin.site.register(Report, ReportAdminConfig)
admin.site.register(Feedback, FeedbackAdminConfig)
admin.site.register(userBook, UserBookAdminConfig)
admin.site.register(userMovie, UserMovieAdminConfig)
admin.site.register(userFeed, UserFeedAdminConfig)
admin.site.register(userReview, UserReviewAdminConfig)
admin.site.register(userGroup, UserGroupAdminConfig)
admin.site.register(groupFeed, GroupFeedAdminConfig)
admin.site.register(groupAdminRequest, GroupAdminApplyConfig)
