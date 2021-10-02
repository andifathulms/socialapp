from django.urls import path

from .views import(
	PostListView,
	PostDetailView,
	PostEditView,
	PostDeleteView,
	CommentDeleteView,
)

app_name = 'post'

urlpatterns = [
	path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
	path('edit/<int:pk>/', PostEditView.as_view(), name='post-edit'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
]