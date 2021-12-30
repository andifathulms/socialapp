from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.urls import reverse_lazy

from .models import Product, ProductImage, ProductCategory, ProductSubCategory, ProductCondition, ProductAvailability
from .forms import ProductForm

from account_profile.models import UserSavedPost

def fillRightNav(request,context):
	user_product = UserSavedPost.objects.get(account = request.user)
	product = user_product.products_saved.all()
	context["products"] = product
	context["type"] = "marketplace"

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
		pass

class MarketplaceDetailView(LoginRequiredMixin, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def get(self, request, pk, *args, **kwargs):
		product = Product.objects.get(pk=pk)

		context = {
			'product': product,
		}

		user_products_saved = UserSavedPost.objects.get(account=request.user)

		is_wishlist = False
		for prod in user_products_saved.products_saved.all():
			if prod == product:
				is_wishlist = True
				break

		context["is_wishlist"] = is_wishlist 
		# fillRightNav(request,context)
		print(context)
		return render(request, 'marketplace/marketplace_detail.html', context)

	def post(self, request, *args, **kwargs):
		
		pass

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
		# fillRightNav(request,context)
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
		# fillRightNav(request,context)
		return render(request, 'marketplace/marketplace.html', context)

class MarketplaceWishlistListView(LoginRequiredMixin, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def get(self, request, *args, **kwargs):
		context = {}

		user_product = UserSavedPost.objects.get(account = request.user)
		product = user_product.products_saved.all()
		category = ProductCategory.objects.all()
		condition = ProductCondition.objects.all()
		
		context["products"] = product
		context["categories"] = category
		context["conditions"] = condition
		context["hide"] = True
		# fillRightNav(request,context)
		return render(request, 'marketplace/marketplace.html', context)

	def post(self, request, *args, **kwargs):
		pass

class MarketplaceManageProductView(LoginRequiredMixin, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def get(self, request, *args, **kwargs):
		logged_in_user = request.user
		context = {}

		product = Product.objects.filter(author=logged_in_user)
		category = ProductCategory.objects.all()
		condition = ProductCondition.objects.all()
		
		context["products"] = product
		context["categories"] = category
		context["conditions"] = condition
		# fillRightNav(request,context)
		return render(request, 'marketplace/marketplace.html', context)

class MarketplaceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('marketplace:marketplace-manage')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class MarketplaceEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'marketplace/marketplace_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('marketplace:marketplace-detail', kwargs={'pk': pk})

    def get_initial(self):
    	initial = super(MarketplaceEditView, self).get_initial()

    	product_object = self.get_object()

    	initial['title'] = product_object.title
    	initial['description'] = product_object.description
    	initial['price'] = product_object.price
    	initial['image'] = product_object.image
    	initial['condition'] = product_object.condition
    	initial['availability'] = product_object.availability
    	initial['location'] = product_object.location
    	initial['category'] = product_object.category
    	print(initial)
    	return initial


    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

@csrf_exempt
def load_subcategories(request):
    category = request.GET.get('category')
    subcategory = ProductSubCategory.objects.filter(category=category).order_by('name')
    
    return render(request, 'marketplace/snippets/subcategory.html', {'subcategories': subcategory})

def onClickWishlist(request):
	
	userProduct = UserSavedPost.objects.get(account=request.user)
	this_product = Product.objects.get(pk=request.GET.get('pk'))

	is_wishlist = False
	for product in userProduct.products_saved.all():
		if product == this_product:
			is_wishlist = True
			break

	if is_wishlist:
		userProduct.products_saved.remove(this_product)
	else:
		userProduct.products_saved.add(this_product)


	return JsonResponse({'data':'OK'})