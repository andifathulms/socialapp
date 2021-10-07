from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation

from notification.models import Notification

class FollowerList(models.Model):

	user 				= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="userfollow")
	followers 			= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="followers") 

	# set up the reverse relation to GenericForeignKey
	notifications		= GenericRelation(Notification)

	def __str__(self):
		return self.user.username

