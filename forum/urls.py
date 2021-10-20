from django.urls import path

from .views import(
	TopicListView,
	)

app_name = 'forum'

urlpatterns = [
	path('topic/', TopicListView.as_view(), name='forum-topic'),
]