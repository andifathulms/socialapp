from django.urls import path

from .views import PostAPIList, PostAPIDetail, CommentAPIDetail

app_name = 'api'

urlpatterns = [
	path('post/', PostAPIList.as_view(), name='api-post-list'),
	path('post/<int:pk>/', PostAPIDetail.as_view(), name='api-post-detail'),
	path('<int:post_pk>/comment/<int:pk>/', CommentAPIDetail.as_view(), name='api-comment-detail'),
]