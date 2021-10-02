from django.db import models
from django.utils import timezone

from account.models import Account

class Post(models.Model):
    body = models.TextField()
    image = models.ImageField(upload_to='uploads/post_photos', blank=True, null=True)
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    likes = models.ManyToManyField(Account, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(Account, blank=True, related_name='dislikes')

class Comment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)