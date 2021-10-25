from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .models import Product, ProductCategory, ProductCondition

class MarketplaceListView(LoginRequiredMixin, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def get(self, request, *args, **kwargs):
		logged_in_user = request.user
		context = {}

		product = Product.objects.all()
		category = ProductCategory.objects.all()
		condition = ProductCondition.objects.all()
		
		context["products"] = product
		context["categories"] = category
		context["conditions"] = condition

		return render(request, 'marketplace/marketplace.html', context)

class MarketplaceDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        product = Product.objects.get(pk=pk)
        
        context = {
            'product': product,
        }

        return render(request, 'marketplace/marketplace_detail.html', context)

