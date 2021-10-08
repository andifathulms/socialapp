from django.urls import path

from follower.views import(
	AddFollower,
	RemoveFollower,
	followers_list_view,
	followings_list_view,
)

app_name = 'follower'

urlpatterns = [
	path('<int:pk>/followers/add/', AddFollower.as_view(), name='follower-add'),
	path('<int:pk>/followers/remove/', RemoveFollower.as_view(), name='follower-remove'),
	path('list/follower/<user_id>', followers_list_view, name='follower-list'),
	path('list/following/<user_id>', followings_list_view, name='following-list'),
]