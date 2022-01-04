from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import redirect
from chat.utils import find_or_create_private_chat

from notification.models import Notification
from account.models import Account

class FollowerList(models.Model):

	user 				= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="userfollow")
	followers 			= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="followers")

	# set up the reverse relation to GenericForeignKey
	notifications		= GenericRelation(Notification)

	def __str__(self):
		return self.user.username

	def add_follower(self, account):
		
		if not account in self.followers.all():
			self.followers.add(account)
			self.save()

			content_type = ContentType.objects.get_for_model(self)

			self.notifications.create(
				target=self.user,
				from_user=account,
				redirect_url=f"{settings.BASE_URL}/account/{account.pk}/",
				verb=f"{account.username} now following you",
				content_type=content_type,
			)
			self.save()
			print("Add Follower")
			chat = find_or_create_private_chat(self.user, account)
			print(chat)
			if not chat.is_active:
				chat.is_active = True
				chat.save()
	
	@property
	def get_cname(self):
		"""
		For determining what kind of object is associated with a Notification
		"""
		return "FollowerList"

class FollowingList(models.Model):

	user 				= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="userfollowing")
	following 			= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="following")

	# set up the reverse relation to GenericForeignKey
	notifications		= GenericRelation(Notification)

	def __str__(self):
		return self.user.username

	def add_following(self, account):

		if not account in self.following.all():
			self.following.add(account)
			self.save()

			content_type = ContentType.objects.get_for_model(self)

			self.notifications.create(
				target=self.user,
				from_user=account,
				redirect_url=f"{settings.BASE_URL}/account/{account.pk}/",
				verb=f"You are now following {account.username}",
				content_type=content_type,
			)
			self.save()

			chat = find_or_create_private_chat(self.user, account)
			if not chat.is_active:
				chat.is_active = True
				chat.save()
	
	@property
	def get_cname(self):
		"""
		For determining what kind of object is associated with a Notification
		"""
		return "FollowingList"



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
