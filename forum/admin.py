from django.contrib import admin

from .models import Subject, ForumPost, ForumReply

admin.site.register(Subject)
admin.site.register(ForumPost)
admin.site.register(ForumReply)