from django.contrib import admin

from .models import FollowerList, FollowingList

admin.site.register(FollowerList)
admin.site.register(FollowingList)
