from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

class TopicListView(LoginRequiredMixin, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'
	def get(self, request, *args, **kwargs):
		logged_in_user = request.user
		context = {}
		return render(request, 'forum/forum_home.html', context)