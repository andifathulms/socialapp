from django.urls import path

from .views import(
	SubjectListView,
	ForumListView,
	ForumDetailView,
	AddUpvote,
	AddDownvote,
	AddReplyUpvote,
	AddReplyDownvote,
	)

app_name = 'forum'

urlpatterns = [
	path('subject/', SubjectListView.as_view(), name='forum-topic'),
	path('content/<int:pk>/', ForumListView.as_view(), name='forum-content'),
	path('detail/<int:pk>/', ForumDetailView.as_view(), name='forum-detail'),
	path('<int:pk>/upvote', AddUpvote.as_view(), name='forum-upvote'),
    path('<int:pk>/downvote', AddDownvote.as_view(), name='forum-downvote'),
    path('<int:post_pk>/reply/<int:pk>/upvote', AddReplyUpvote.as_view(), name='reply-upvote'),
    path('<int:post_pk>/reply/<int:pk>/downvote', AddReplyDownvote.as_view(), name='reply-downvote'),
]