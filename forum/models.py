from django.db import models
from django.utils import timezone

from mptt.models import MPTTModel, TreeForeignKey

from account.models import Account

class Subject(models.Model):

	title = models.CharField(max_length=100)
	type = models.CharField(max_length=20, blank=True, null=True)
	created_on = models.DateTimeField(default=timezone.now)
	description = models.TextField()
	admin = models.ManyToManyField(Account, blank=True, related_name='forum_admin')
	image = models.ImageField(upload_to='uploads/subject_img/', blank=True, null=True)
	subscriber = models.ManyToManyField(Account, blank=True, related_name='forum_subscriber')

class ForumPost(models.Model):

	title = models.CharField(max_length=200)
	body = models.TextField()
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True)
	created_on = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(Account, on_delete=models.CASCADE)
	upvote = models.ManyToManyField(Account, blank=True, related_name='upvote')
	downvote = models.ManyToManyField(Account, blank=True, related_name='downvote')
	view = models.IntegerField(default=1)

class ForumReply(MPTTModel):

	reply = models.TextField()
	created = models.DateTimeField(default=timezone.now)
	post = models.ForeignKey('ForumPost', on_delete=models.CASCADE)
	author = models.ForeignKey(Account, on_delete=models.CASCADE)
	upvote = models.ManyToManyField(Account, blank=True, related_name='upvote_reply')
	downvote = models.ManyToManyField(Account, blank=True, related_name='downvote_reply')
	parent = TreeForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='children')
	reply_to = models.ForeignKey(Account, null=True, blank=True, on_delete=models.CASCADE, related_name='replyers')

	class MPTTMeta:
		order_insertion_by = ['created']