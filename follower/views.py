from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from follower.models import FollowerList
from account_profile.models import UserProfile

class AddFollower(LoginRequiredMixin, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'
	
	def post(self, request, pk, *args, **kwargs):
		for x in FollowerList.objects.all():
			print(x.pk)
			print(x.user.username)
			print(x.user.pk)
		follower_list = FollowerList.objects.get(pk=pk)
		follower_list.followers.add(request.user)

		profile = UserProfile.objects.get(account=follower_list.user)

		return redirect('account:view', profile.pk)

class RemoveFollower(LoginRequiredMixin, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'
	
	def post(self, request, pk, *args, **kwargs):
		for x in FollowerList.objects.all():
			print(x.pk)
			print(x.user.username)
			print(x.user.pk)
		follower_list = FollowerList.objects.get(pk=pk)
		follower_list.followers.remove(request.user)

		profile = UserProfile.objects.get(account=follower_list.user)

		return redirect('account:view', profile.pk)