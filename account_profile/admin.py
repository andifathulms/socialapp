from django.contrib import admin

from .models import UserProfile, UserSavedPost, Occupation, Prodi

admin.site.register(UserProfile)
admin.site.register(UserSavedPost)
admin.site.register(Occupation)
admin.site.register(Prodi)
