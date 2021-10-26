from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Product, ProductImage, ProductCategory, ProductSubCategory, ProductCondition, ProductAvailability
from .forms import ProductForm

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

	def post(self, request, *args, **kwargs):
		print("list")

class MarketplaceDetailView(LoginRequiredMixin, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def get(self, request, pk, *args, **kwargs):
		product = Product.objects.get(pk=pk)

		context = {
			'product': product,
		}

		return render(request, 'marketplace/marketplace_detail.html', context)

	def post(self, request, *args, **kwargs):
		print("det")

class MarketplaceCreateView(LoginRequiredMixin, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def get(self, request, *args, **kwargs):
		condition = ProductCondition.objects.all()
		availability = ProductAvailability.objects.all()
		categories = ProductCategory.objects.all()

		context = {}
		context["conditions"] = condition
		context["availabilities"] = availability
		context["categories"] = categories

		return render(request, 'marketplace/marketplace_create.html', context)

	def post(self, request, *args, **kwargs):
		form = ProductForm(request.POST, request.FILES)
		files = request.FILES.getlist('image')
		
		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.author = request.user
			new_post.save()

			for f in files:
				img = ProductImage(image=f)
				img.save()
				new_post.image.add(img)
		
		else:
			print(form.errors)

		context = {}

		product = Product.objects.all()
		category = ProductCategory.objects.all()
		condition = ProductCondition.objects.all()

		context["products"] = product
		context["categories"] = category
		context["conditions"] = condition

		return render(request, 'marketplace/marketplace.html', context)

@csrf_exempt
def load_subcategories(request):
    category = request.GET.get('category')
    subcategory = ProductSubCategory.objects.filter(category=category).order_by('name')
    print(subcategory)
    return render(request, 'marketplace/snippets/subcategory.html', {'subcategories': subcategory})

