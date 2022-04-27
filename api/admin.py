from django.contrib import admin
from .models.users import CustomUser
from .models.books import Book
from .models.movies import Movie
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Book)
admin.site.register(Movie)