from django.contrib import admin
from .models.users import CustomUser
from .models.books import Book
from .models.movies import Movie
# Register your models here.

class UserAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')

class BookAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'isbn', 'title', 'year')

class MovieAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'title', 'year')


admin.site.register(CustomUser, UserAdminConfig)
admin.site.register(Book, BookAdminConfig)
admin.site.register(Movie, MovieAdminConfig)