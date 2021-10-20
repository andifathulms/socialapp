from django.db import models
from django.utils import timezone

from account.models import Account

class Subject(models.Model):

	title = models.CharField(max_length=100)
	created_on = models.DateTimeField(default=timezone.now)
	description = models.TextField()
	admin = models.ManyToManyField(Account, blank=True, related_name='forum_admin')


class ForumPost(models.Model):

	title = models.CharField(max_length=200)
	body = models.TextField()
	created_on = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(Account, on_delete=models.CASCADE)
	upvote = models.ManyToManyField(Account, blank=True, related_name='upvote')
	downvote = models.ManyToManyField(Account, blank=True, related_name='downvote')
	view = models.IntegerField(default=0)

class ForumReply(models.Model):

	reply = models.TextField()
	created_on = models.DateTimeField(default=timezone.now)
	post = models.ForeignKey('ForumPost', on_delete=models.CASCADE)
	author = models.ForeignKey(Account, on_delete=models.CASCADE)
	upvote = models.ManyToManyField(Account, blank=True, related_name='upvote_reply')
	downvote = models.ManyToManyField(Account, blank=True, related_name='downvote_reply')
