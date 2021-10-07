from django.urls import path

from follower.views import(
	AddFollower,
	RemoveFollower
)

app_name = 'follower'

urlpatterns = [
	path('<int:pk>/followers/add/', AddFollower.as_view(), name='follower-add'),
	path('<int:pk>/followers/remove/', RemoveFollower.as_view(), name='follower-remove'),
]