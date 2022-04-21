from django.contrib import admin
from .models.users import CustomUser

# Register your models here.

admin.site.register(CustomUser)