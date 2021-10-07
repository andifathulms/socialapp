from django.urls import path

from .views import(
	PostListView,
	PostDetailView,
	PostEditView,
	PostDeleteView,
	CommentDeleteView,
	AddLike,
	AddDislike,
)

app_name = 'post'

urlpatterns = [
	path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
	path('edit/<int:pk>/', PostEditView.as_view(), name='post-edit'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('<int:pk>/like', AddLike.as_view(), name='post-like'),
    path('<int:pk>/dislike', AddDislike.as_view(), name='post-dislike'),
]