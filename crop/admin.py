# crop/admin.py
from django.contrib import admin
from .models import Soildata, Article, Profile

# Register your models with the admin site
admin.site.register(Soildata)
admin.site.register(Article)
admin.site.register(Profile)