from django.urls import path

from .views import(
	MarketplaceListView,
	)

app_name = 'marketplace'

urlpatterns = [
	path('', MarketplaceListView.as_view(), name='marketplace-home'),
]