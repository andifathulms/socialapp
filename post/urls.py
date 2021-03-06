from django.urls import path

from .views import(
	PostListView,
	PostDetailView,
	PostEditView,
	PostEditViewHTMX,
	PostDeleteView,
	CommentEditViewHTMX,
	CommentDeleteView,
	AddLike,
	AddDislike,
	AddCommentLike, 
	AddCommentDislike, 
	CommentReplyView,
	SharedPostView,
	LoadUrlPreview,
)

app_name = 'post'

urlpatterns = [
	path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
	path('edit/<int:pk>/', PostEditViewHTMX.as_view(), name='post-edit'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('<int:post_pk>/comment/edit/<int:pk>/', CommentEditViewHTMX.as_view(), name='comment-edit'),
    path('<int:pk>/like', AddLike.as_view(), name='post-like'),
    path('<int:pk>/dislike', AddDislike.as_view(), name='post-dislike'),
    path('<int:post_pk>/comment/<int:pk>/like', AddCommentLike.as_view(), name='comment-like'),
    path('<int:post_pk>/comment/<int:pk>/dislike', AddCommentDislike.as_view(), name='comment-dislike'),
    path('<int:post_pk>/comment/<int:pk>/reply', CommentReplyView.as_view(), name='comment-reply'),
    path('<int:pk>/share', SharedPostView.as_view(), name='share-post'),
    path('load-url-preview/<int:pk>/', LoadUrlPreview.as_view(), name='load-url-preview'),
]