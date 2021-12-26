from django.db import models
from django.utils import timezone

from account.models import Account

class Product(models.Model):
	
	title = models.CharField(max_length=100)
	description = models.TextField()
	price = models.IntegerField()
	image = models.ManyToManyField('ProductImage', blank=True)
	created_on = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(Account, on_delete=models.CASCADE)
	category = models.ForeignKey('ProductSubCategory', on_delete=models.CASCADE)
	condition = models.ForeignKey('ProductCondition', on_delete=models.CASCADE)
	availability = models.ForeignKey('ProductAvailability', on_delete=models.CASCADE)
	location = models.CharField(max_length=200)
	view = models.IntegerField(default=1)
	
	def __str__(self):
		return self.title

class ProductImage(models.Model):
    image = models.ImageField(upload_to='uploads/marketplace_photos/', blank=True, null=True)

class ProductCategory(models.Model):
	name = models.CharField(max_length=100)

class ProductSubCategory(models.Model):
	category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)

class ProductCondition(models.Model):
	name = models.CharField(max_length=100)

class ProductAvailability(models.Model):
	name = models.CharField(max_length=100)