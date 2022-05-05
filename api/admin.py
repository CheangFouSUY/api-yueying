from django.contrib import admin

from .models.feedbacks import Feedback
from .models.reports import Report
from .models.users import CustomUser
from .models.books import Book
from .models.movies import Movie
from .models.groups import Group
from .models.feeds import Feed
from .models.reviews import Review
# Register your models here.

class UserAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')

class BookAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'isbn', 'title', 'year')

class MovieAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'title', 'year')

class GroupAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'groupName', 'category','createdBy')

class FeedAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'title', 'isPublic','createdBy', 'belongTo')

class ReviewAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'title', 'createdBy')

class ReportAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'title', 'category','createdBy','result')

class FeedbackAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'title', 'createdBy')

admin.site.register(CustomUser, UserAdminConfig)
admin.site.register(Book, BookAdminConfig)
admin.site.register(Movie, MovieAdminConfig)
admin.site.register(Group, GroupAdminConfig)
admin.site.register(Feed, FeedAdminConfig)
admin.site.register(Review, ReviewAdminConfig)
admin.site.register(Report, ReportAdminConfig)
admin.site.register(Feedback, FeedbackAdminConfig)