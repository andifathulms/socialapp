from django.urls import path

from .views import(
	MarketplaceListView,
	MarketplaceDetailView,
	MarketplaceCreateView,
	MarketplaceWishlistListView,
	MarketplaceManageProductView,
	MarketplaceDeleteView,
	MarketplaceEditView,
	load_subcategories,
	onClickWishlist,
	)

app_name = 'marketplace'

urlpatterns = [
	path('', MarketplaceListView.as_view(), name='marketplace-home'),
	path('<int:pk>/', MarketplaceDetailView.as_view(), name='marketplace-detail'),
	path('create/', MarketplaceCreateView.as_view(), name='marketplace-create'),
	path('wishlist/', MarketplaceWishlistListView.as_view(), name='marketplace-wishlist'),
	path('manage/', MarketplaceManageProductView.as_view(), name='marketplace-manage'),
	path('delete/<int:pk>/', MarketplaceDeleteView.as_view(), name='marketplace-delete'),
	path('edit/<int:pk>/', MarketplaceEditView.as_view(), name='marketplace-edit'),
	path('ajax/load-cat/', load_subcategories, name='ajax_load_subcat'),
	path('ajax/wishlist/', onClickWishlist, name='ajax_wishlist'),
]
