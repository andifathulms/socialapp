from django.urls import path

from .views import PostAPIList, PostAPIDetail

app_name = 'api'

urlpatterns = [
	path('post/', PostAPIList.as_view(), name='api-post-list'),
	path('post/<int:pk>/', PostAPIDetail.as_view(), name='api-post-detail'),
]