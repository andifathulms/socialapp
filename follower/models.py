from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.signals import post_save
from django.dispatch import receiver

from notification.models import Notification
from account.models import Account

class FollowerList(models.Model):

	user 				= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="userfollow")
	followers 			= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="followers")

	# set up the reverse relation to GenericForeignKey
	notifications		= GenericRelation(Notification)

	def __str__(self):
		return self.user.username

class FollowingList(models.Model):

	user 				= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="userfollowing")
	following 			= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="following")

	# set up the reverse relation to GenericForeignKey
	notifications		= GenericRelation(Notification)

	def __str__(self):
		return self.user.username

@receiver(post_save, sender=Account)
def create_follower_list(sender, instance, created, **kwargs):
	if created:
		FollowerList.objects.create(user=instance)

@receiver(post_save, sender=Account)
def create_following_list(sender, instance, created, **kwargs):
	if created:
		FollowingList.objects.create(user=instance)

@receiver(post_save, sender=Account)
def save_follower_list(sender, instance, **kwargs):
	instance.profile.save()

@receiver(post_save, sender=Account)
def save_following_list(sender, instance, **kwargs):
	instance.profile.save() 
