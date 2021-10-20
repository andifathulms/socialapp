from django.urls import path

from .views import(
	SubjectListView,
	ForumListView,
	ForumDetailView,
	)

app_name = 'forum'

urlpatterns = [
	path('subject/', SubjectListView.as_view(), name='forum-topic'),
	path('content/<int:pk>/', ForumListView.as_view(), name='forum-content'),
	path('detail/<int:pk>/', ForumDetailView.as_view(), name='forum-detail'),
]