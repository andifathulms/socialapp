from django.urls import path

from .views import(
        the2048View,
        the2048Leaderboard,
	)

app_name = 'games'

urlpatterns = [
	path('2048/', the2048View.as_view(), name='g-2048'),
    path('2048/leaderboard', the2048Leaderboard.as_view(), name='g-2048-leaderboard'),
]