from django.urls import path

from .views import(
	MarketplaceListView,
	MarketplaceDetailView,
	MarketplaceCreateView,
	MarketplaceWishlistListView,
	load_subcategories,
	onClickWishlist,
	)

app_name = 'marketplace'

urlpatterns = [
	path('', MarketplaceListView.as_view(), name='marketplace-home'),
	path('<int:pk>/', MarketplaceDetailView.as_view(), name='marketplace-detail'),
	path('create/', MarketplaceCreateView.as_view(), name='marketplace-create'),
	path('wishlist/', MarketplaceWishlistListView.as_view(), name='marketplace-wishlist'),
	path('ajax/load-cat/', load_subcategories, name='ajax_load_subcat'),
	path('ajax/wishlist/', onClickWishlist, name='ajax_wishlist'),
]
