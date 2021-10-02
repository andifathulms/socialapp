from django.urls import path

from public_chat.views import(
	public_chat_view,
)

app_name = 'public_chat'

urlpatterns = [
	path('', public_chat_view, name='public_chat_room'),
]