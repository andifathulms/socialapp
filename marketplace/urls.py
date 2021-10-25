from django.urls import path

from .views import(
	MarketplaceListView,
	MarketplaceDetailView,
	)

app_name = 'marketplace'

urlpatterns = [
	path('', MarketplaceListView.as_view(), name='marketplace-home'),
	path('<int:pk>/', MarketplaceDetailView.as_view(), name='marketplace-detail'),
]