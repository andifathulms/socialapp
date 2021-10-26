from django.urls import path

from .views import(
	MarketplaceListView,
	MarketplaceDetailView,
	MarketplaceCreateView,
	load_subcategories,
	)

app_name = 'marketplace'

urlpatterns = [
	path('', MarketplaceListView.as_view(), name='marketplace-home'),
	path('<int:pk>/', MarketplaceDetailView.as_view(), name='marketplace-detail'),
	path('create/', MarketplaceCreateView.as_view(), name='marketplace-create'),
	path('ajax/load-cat/', load_subcategories, name='ajax_load_subcat'),
]