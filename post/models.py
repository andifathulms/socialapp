from django.db import models
from django.utils import timezone

from account.models import Account

class Post(models.Model):
    body = models.TextField()
    image = models.ManyToManyField('Image', blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    likes = models.ManyToManyField(Account, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(Account, blank=True, related_name='dislikes')
    shared_body = models.TextField(blank=True, null=True)
    shared_on = models.DateTimeField(blank=True, null=True)
    shared_user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True, related_name='+')

    class Meta:
        ordering = ['-created_on', '-shared_on']

class Comment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    likes = models.ManyToManyField(Account, blank=True, related_name='comment_likes')
    dislikes = models.ManyToManyField(Account, blank=True, related_name='comment_dislikes')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')

    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-created_on').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

class Image(models.Model):
    image = models.ImageField(upload_to='uploads/post_photos/', blank=True, null=True)