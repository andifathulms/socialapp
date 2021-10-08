from django.urls import path

from .views import(
	PostListView,
	PostDetailView,
	PostEditView,
	PostDeleteView,
	CommentDeleteView,
	AddLike,
	AddDislike,
	AddCommentLike, 
	AddCommentDislike, 
	CommentReplyView,
	SharedPostView,
)

app_name = 'post'

urlpatterns = [
	path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
	path('edit/<int:pk>/', PostEditView.as_view(), name='post-edit'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('<int:pk>/like', AddLike.as_view(), name='post-like'),
    path('<int:pk>/dislike', AddDislike.as_view(), name='post-dislike'),
    path('<int:post_pk>/comment/<int:pk>/like', AddCommentLike.as_view(), name='comment-like'),
    path('<int:post_pk>/comment/<int:pk>/dislike', AddCommentDislike.as_view(), name='comment-dislike'),
    path('<int:post_pk>/comment/<int:pk>/reply', CommentReplyView.as_view(), name='comment-reply'),
    path('<int:pk>/share', SharedPostView.as_view(), name='share-post'),
]