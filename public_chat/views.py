from django.shortcuts import render
from django.conf import settings

DEBUG = False

def public_chat_view(request):
	context = {}
	context['debug_mode'] = settings.DEBUG
	context['debug'] = DEBUG
	context['room_id'] = "1"
	return render(request, "public_chat/room.html", context)
