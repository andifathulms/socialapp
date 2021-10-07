from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required

DEBUG = False

@login_required
def home_screen_view(request):
	context = {}
	context['debug_mode'] = settings.DEBUG
	context['debug'] = DEBUG
	context['room_id'] = "1"
	return render(request, "personal/home.html", context)

