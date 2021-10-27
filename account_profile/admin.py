from django.contrib import admin

from .models import UserProfile, UserSavedPost

admin.site.register(UserProfile)
admin.site.register(UserSavedPost)
