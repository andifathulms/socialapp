from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path, re_path

from public_chat.consumers import PublicChatConsumer
from chat.consumers import ChatConsumer

application = ProtocolTypeRouter({
	'websocket': AllowedHostsOriginValidator(
		AuthMiddlewareStack(
			URLRouter([
					path('chat/<room_id>/', ChatConsumer.as_asgi()),
					path('public_chat/<room_id>/', PublicChatConsumer.as_asgi()), #as_asgi() added
			])
		)
	),
})