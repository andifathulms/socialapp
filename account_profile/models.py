from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import Account
from marketplace.models import Product

class UserProfile(models.Model):
	account 	= models.OneToOneField(Account, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
	fullname	= models.CharField(max_length=100, blank=True, null=True)
	bio 		= models.TextField(max_length=500,default="Apparently, this user prefers to keep an air of mystery about them.", blank=True, null=True)
	phone		= models.CharField(max_length=15, blank=True, null=True)
	hobby 		= models.CharField(max_length=100, blank=True, null=True)
	birth_date	= models.DateField(null=True, blank=True)
	birth_place	= models.CharField(max_length=100, null=True, blank=True)
	location 	= models.CharField(max_length=100, blank=True, null=True)
	accWebsite	= models.CharField(max_length=200, blank=True, null=True)
	accGithub	= models.CharField(max_length=200, blank=True, null=True)
	accTwitter	= models.CharField(max_length=200, blank=True, null=True)
	accInsta	= models.CharField(max_length=200, blank=True, null=True)
	accFacebook	= models.CharField(max_length=200, blank=True, null=True)
	schoolSD	= models.CharField(max_length=200, blank=True, null=True)
	schoolSMP	= models.CharField(max_length=200, blank=True, null=True)
	schoolSMA	= models.CharField(max_length=200, blank=True, null=True)
	status		= models.CharField(max_length=50, blank=True, null=True)
	nobp		= models.CharField(max_length=20, blank=True, null=True)
	prodi		= models.CharField(max_length=50, blank=True, null=True)

class UserSavedPost(models.Model):
	account        = models.OneToOneField(Account, primary_key=True, on_delete=models.CASCADE, related_name='user_wish')
	products_saved = models.ManyToManyField(Product, blank=True)


@receiver(post_save, sender=Account)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(account=instance)

@receiver(post_save, sender=Account)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

@receiver(post_save, sender=Account)
def create_user_saved_post(sender, instance, created, **kwargs):
	if created:
		UserSavedPost.objects.create(account=instance)

@receiver(post_save, sender=Account)
def save_user_saved_post(sender, instance, **kwargs):
	instance.profile.save() 