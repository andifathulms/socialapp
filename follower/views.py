from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from follower.models import FollowerList, FollowingList
from friend.models import FriendList
from account.models import Account
from account_profile.models import UserProfile

from post.views import fillRightNav

class AddFollower(LoginRequiredMixin, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'
	
	def post(self, request, pk, *args, **kwargs):
		context = {}
		reqUser = Account.objects.get(pk=pk)

		follower_list = FollowerList.objects.get(user=reqUser)
		#follower_list.followers.add(request.user)
		follower_list.add_follower(request.user)

		following_list = FollowingList.objects.get(user=request.user)
		#following_list.following.add(reqUser)
		following_list.add_following(reqUser)
		context["result"] = reqUser
		return render(request, 'follower/snippets/span_btn_followed.html', context)

class RemoveFollower(LoginRequiredMixin, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'
	
	def post(self, request, pk, *args, **kwargs):
		context = {}
		reqUser = Account.objects.get(pk=pk)
		follower_list = FollowerList.objects.get(user=reqUser)
		follower_list.followers.remove(request.user)

		following_list = FollowingList.objects.get(user=request.user)
		following_list.following.remove(reqUser)
		context["result"] = reqUser
		return render(request, 'follower/snippets/span_btn_following.html', context)

class FollowerListView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		user_id = kwargs.get("user_id")
		context = {}
		user = Account.objects.get(pk=user_id)
		followerlist = FollowerList.objects.get(user=user)
		# followers = followerlist.followers
		context["followers"] = followerlist
		fillRightNav(request,context)
		return render(request, 'follower/follower_list_2.html', context)

class FollowingListView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		user_id = kwargs.get("user_id")
		context = {}
		user = Account.objects.get(pk=user_id)
		followinglist = FollowingList.objects.get(user=user)
		print(followinglist)
		# followers = followerlist.followers
		context["followings"] = followinglist
		fillRightNav(request,context)
		return render(request, 'follower/follower_list_2.html', context)

def followers_list_view(request, *args, **kwargs):
	context = {}
	user = request.user
	if user.is_authenticated:
		user_id = kwargs.get("user_id")
		if user_id:
			try:
				this_user = Account.objects.get(pk=user_id)
				context['this_user'] = this_user
			except Account.DoesNotExist:
				return HttpResponse("That user does not exist.")
			try:
				friend_list = FriendList.objects.get(user=this_user)
			except FriendList.DoesNotExist:
				return HttpResponse(f"Could not find a friends list for {this_user.username}")

			try:
				follower_list = FollowerList.objects.get(user=this_user)
			except FollowerList.DoesNotExist:
				return HttpResponse(f"Could not find a followers list for {this_user.username}")

			friends = [] # [(friend1, True), (friend2, False), ...]
			# get the authenticated users friend list
			auth_user_friend_list = FriendList.objects.get(user=user)
			for follower in follower_list.followers.all():
				profile = UserProfile.objects.get(account=follower)

				#get all of the follower friends
				try:
					friend_list_sec = FriendList.objects.get(user=follower)
				except FriendList.DoesNotExist:
					friend_list_sec = FriendList(user=follower)
					friend_list_sec.save()
				friends_sec = friend_list_sec.friends.all()

				#get all of the follower followers
				try:
					followers_list_sec = FollowerList.objects.get(user=follower)
				except FollowerList.DoesNotExist:
					followers_list_sec = FollowerList(user=follower)
					followers_list_sec.save()
				followers_sec = followers_list_sec.followers.all()

				#get all of the follower followings
				try:
					following_list_sec = FollowingList.objects.get(user=follower)
				except FollowingList.DoesNotExist:
					following_list_sec = FollowingList(user=follower)
					following_list_sec.save()
				followings_sec = following_list_sec.following.all()

				friends.append((follower, auth_user_friend_list.is_mutual_friend(follower),profile, friends_sec, followers_sec, followings_sec))
			context['friends'] = friends
			context['this_user'] = this_user
	else:		
		return HttpResponse("You must be friends to view their friends list.")
	return render(request, "follower/follower_list.html", context)

def followings_list_view(request, *args, **kwargs):
	context = {}
	user = request.user
	if user.is_authenticated:
		user_id = kwargs.get("user_id")
		if user_id:
			try:
				this_user = Account.objects.get(pk=user_id)
				context['this_user'] = this_user
			except Account.DoesNotExist:
				return HttpResponse("That user does not exist.")
			try:
				friend_list = FriendList.objects.get(user=this_user)
			except FriendList.DoesNotExist:
				return HttpResponse(f"Could not find a friends list for {this_user.username}")

			try:
				following_list = FollowingList.objects.get(user=this_user)
			except FollowingList.DoesNotExist:
				return HttpResponse(f"Could not find a followers list for {this_user.username}")

			friends = [] # [(friend1, True), (friend2, False), ...]
			# get the authenticated users friend list
			auth_user_friend_list = FriendList.objects.get(user=user)
			for follower in following_list.following.all():
				profile = UserProfile.objects.get(account=follower)

				#get all of the follower friends
				try:
					friend_list_sec = FriendList.objects.get(user=follower)
				except FriendList.DoesNotExist:
					friend_list_sec = FriendList(user=follower)
					friend_list_sec.save()
				friends_sec = friend_list_sec.friends.all()

				#get all of the follower followers
				try:
					followers_list_sec = FollowerList.objects.get(user=follower)
				except FollowerList.DoesNotExist:
					followers_list_sec = FollowerList(user=follower)
					followers_list_sec.save()
				followers_sec = followers_list_sec.followers.all()

				#get all of the follower followings
				try:
					following_list_sec = FollowingList.objects.get(user=follower)
				except FollowingList.DoesNotExist:
					following_list_sec = FollowingList(user=follower)
					following_list_sec.save()
				followings_sec = following_list_sec.following.all()

				friends.append((follower, auth_user_friend_list.is_mutual_friend(follower),profile, friends_sec, followers_sec, followings_sec))
			context['friends'] = friends
			context['this_user'] = this_user
	else:		
		return HttpResponse("You must be friends to view their friends list.")
	return render(request, "follower/following_list.html", context)