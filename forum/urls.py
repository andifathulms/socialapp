from django.urls import path

from .views import(
	SubjectListView,
	ForumListView,
	ForumDetailView,
	AddUpvote,
	AddDownvote,
	AddReplyUpvote,
	AddReplyDownvote,
	AddSubscribe,
	UpvoteForumPostList,
	DownvoteForumPostList,
	ChangeRightNav1,
	ChangeRightNav2,
	ChangeRightNav0,
	)

app_name = 'forum'

urlpatterns = [
	path('subject/', SubjectListView.as_view(), name='forum-topic'),
	path('subscribe/<int:pk>/', AddSubscribe.as_view(), name='forum-subscribe'),
	path('content/<int:pk>/', ForumListView.as_view(), name='forum-content'),
	path('detail/<int:pk>/', ForumDetailView.as_view(), name='forum-detail'),
	path('detail/<int:pk>/<int:parent_comment_id>', ForumDetailView.as_view(), name='forum-detail-reply'),
	path('<int:pk>/upvote', AddUpvote.as_view(), name='forum-upvote'),
    path('<int:pk>/downvote', AddDownvote.as_view(), name='forum-downvote'),
    path('<int:post_pk>/reply/<int:pk>/upvote', AddReplyUpvote.as_view(), name='reply-upvote'),
    path('<int:post_pk>/reply/<int:pk>/downvote', AddReplyDownvote.as_view(), name='reply-downvote'),
    path('upvote-from-post/<int:pk>/', UpvoteForumPostList.as_view(), name='upvote-from-post'),
    path('downvote-from-post/<int:pk>/', DownvoteForumPostList.as_view(), name='downvote-from-post'),
    path('change-right-nav-1/', ChangeRightNav1.as_view(), name='change-right-nav-1'),
    path('change-right-nav-2/', ChangeRightNav2.as_view(), name='change-right-nav-2'),
    path('change-right-nav-0/', ChangeRightNav0.as_view(), name='change-right-nav-0'),
]