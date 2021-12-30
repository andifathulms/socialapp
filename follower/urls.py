from django.urls import path

from follower.views import(
	AddFollower,
	RemoveFollower,
	FollowerListView,
	FollowingListView,
)

app_name = 'follower'

urlpatterns = [
	path('<int:pk>/followers/add/', AddFollower.as_view(), name='follower-add'),
	path('<int:pk>/followers/remove/', RemoveFollower.as_view(), name='follower-remove'),
	path('list/follower/<user_id>', FollowerListView.as_view(), name='follower-list'),
	path('list/following/<user_id>', FollowingListView.as_view(), name='following-list'),
]