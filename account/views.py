from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings

from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from django.core import files

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import os
import cv2
import json
import base64
import requests

from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from account.models import Account

from account_profile.models import UserProfile, Occupation, Prodi
from account_profile.forms import ProfileUpdateForm, InitialProfileForm

from post.models import Post

from friend.utils import get_friend_request_or_false
from friend.friend_request_status import FriendRequestStatus
from friend.models import FriendList, FriendRequest

from follower.models import FollowerList, FollowingList

from blog.models import Blog
from forum.models import ForumPost, ForumReply

from itertools import chain
from operator import attrgetter
from django.db.models import Q

from post.views import fillRightNav

import string    
import random

TEMP_PROFILE_IMAGE_NAME = "temp_profile_image.png"

def register_view(request, *args, **kwargs):
	user = request.user
	if user.is_authenticated: 
		return HttpResponse("You are already authenticated as " + str(user.email))

	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email').lower()
			raw_password = form.cleaned_data.get('password1')

			account = authenticate(email=email, password=raw_password)
			login(request, account)

			destination = kwargs.get("next")
			if destination:
				return redirect(destination)
			return redirect('home')
		else:
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'account/register.html', context)

def logout_view(request):
	print(request.user.email)
	logout(request)
	return redirect("home")


def login_view(request, *args, **kwargs):
	context = {}

	if request.POST and 'btnInitial' in request.POST:
		print("POST and regis")
		form = InitialProfileForm(request.POST, instance=request.user)
		data = request.POST
		if form.is_valid():
			profile = UserProfile.objects.get(account=request.user)
			profile.fullname = data["fullname"]
			profile.birth_date = data["birth_date"]
			profile.occupation  = Occupation.objects.get(pk=data["occupation"])
			profile.save()
			print(data["fullname"])
			destination = kwargs.get("next")
			if destination:
				return redirect(destination)
			return redirect('home')
		else:
			print(form.errors)
			context['registration_form'] = form
			context['initial_form'] = form
	
	user = request.user
	if user.is_authenticated: 
		return redirect("home")
	
	destination = get_redirect_if_exists(request)
	print("destination: " + str(destination))

	if request.htmx:
		print("htmx")
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email').lower()
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			
			#Assign random fullname for the first time
			profile = UserProfile.objects.get(account=account)
			S = 10
			ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))
			profile.fullname = "user-" + str(ran)
			profile.save()

			admin = Account.objects.get(pk=1)
			profile.create_notif_first_login(admin)

			context["occupations"] = Occupation.objects.all()
			return render(request, "account/initial_profile.html", context)
		else:
			print(form.errors)
			context['registration_form'] = form
			return render(request, 'account/login.html', context)

	if request.POST:
		print("POST only")
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				if destination:
					return redirect(destination)
				return redirect("home")

	else:
		print("else POST only")
		form = AccountAuthenticationForm()
	
	context['login_form'] = form
	# if request.htmx:
	# 	return render(request, 'account/login.html', context)
	print("Overflow")
	return render(request, "base_2.html", context)

def lock_view(request):
	context = {}
	redirect_to = request.GET.get('next', '')

	try:
		response = render(request, "page-lock.html", context)
		response.set_cookie('email',request.user.email)
		response.set_cookie('username',request.user.username)
		
		logout(request)
	except:
		response = render(request, "page-lock.html", context)

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		print(form.errors)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return HttpResponseRedirect(redirect_to)

	return response

def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect

@login_required
def account_view(request, *args, **kwargs):
	"""
	- Logic here is kind of tricky
		is_self (boolean)
			is_friend (boolean)
				-1: NO_REQUEST_SENT
				0: THEM_SENT_TO_YOU
				1: YOU_SENT_TO_THEM
	"""
	context = {}
	user_id = kwargs.get("user_id")
	try:
		account = Account.objects.get(pk=user_id)
		profile = UserProfile.objects.get(account=account)
		posts   = Post.objects.filter(author=account).order_by('-created_on')

	except:
		return HttpResponse("Something went wrong.")
	if account:
		context['id'] = account.id
		context['username'] = account.username
		context['email'] = account.email
		context['profile_image'] = account.profile_image.url
		context['hide_email'] = account.hide_email
		context['date_joined'] = account.date_joined
		context['last_login'] = account.last_login

		context['fullname'] = profile.fullname
		context['bio'] = profile.bio
		context['phone'] = profile.phone
		context['hobby'] = profile.hobby
		context['birth_date'] = profile.birth_date
		context['birth_place'] = profile.birth_place
		context['location'] = profile.location
		context['accWebsite'] = profile.accWebsite
		context['accGithub'] = profile.accGithub
		context['accTwitter'] = profile.accTwitter
		context['accInsta'] = profile.accInsta
		context['accFacebook'] = profile.accFacebook
		context['schoolSD'] = profile.schoolSD
		context['schoolSMP'] = profile.schoolSMP
		context['schoolSMA'] = profile.schoolSMA
		context['status'] = profile.status
		context['nobp'] = profile.nobp
		context['prodi'] = profile.prodi

		context["account"] = account
		context["profile"] = profile

		try:
			friend_list = FriendList.objects.get(user=account)
		except FriendList.DoesNotExist:
			friend_list = FriendList(user=account)
			friend_list.save()
		friends = friend_list.friends.all()
		context['friends'] = friends

		try:
			follower_list = FollowerList.objects.get(user=account)
		except FollowerList.DoesNotExist:
			follower_list = FollowerList(user=account)
			follower_list.save()
		followers = follower_list.followers.all()
		context['followers'] = followers
		context['follower_list'] = follower_list

		try:
			following_list = FollowingList.objects.get(user=account)
		except FollowingList.DoesNotExist:
			following_list = FollowingList(user=account)
			following_list.save()
		followings = following_list.following.all()
		context['followings'] = followings
		context['followings_list'] = following_list

		if len(followers) == 0:
			is_following = False

		for follower in followers:
			if follower == request.user:
				is_following = True
				break
			else:
				is_following = False

		context['is_following'] = is_following

		# Define template variables
		is_self = True
		is_friend = False
		request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
		friend_requests = None
		user = request.user
		if user.is_authenticated and user != account:
			is_self = False
			if friends.filter(pk=user.id):
				is_friend = True
			else:
				is_friend = False
				# CASE1: Request has been sent from THEM to YOU: FriendRequestStatus.THEM_SENT_TO_YOU
				if get_friend_request_or_false(sender=account, receiver=user) != False:
					request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
					context['pending_friend_request_id'] = get_friend_request_or_false(sender=account, receiver=user).id
				# CASE2: Request has been sent from YOU to THEM: FriendRequestStatus.YOU_SENT_TO_THEM
				elif get_friend_request_or_false(sender=user, receiver=account) != False:
					request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
				# CASE3: No request sent from YOU or THEM: FriendRequestStatus.NO_REQUEST_SENT
				else:
					request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
		elif not user.is_authenticated:
			is_self = False
		else:
			try:
				friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
			except:
				pass
			
		# Set the template variables to the values
		context['is_self'] = is_self
		context['is_friend'] = is_friend
		context['request_sent'] = request_sent
		context['friend_requests'] = friend_requests
		context['BASE_URL'] = settings.BASE_URL
		
		join_paginator = Paginator(posts,10)
		page = request.GET.get('page', 1)
		
		try:
			join_pagination = join_paginator.page(page)
		except PageNotAnInteger:
			join_pagination = join_paginator.page(1)
		except EmptyPage:
			join_pagination = join_paginator.page(join_paginator.num_pages)
		
		context['posts'] = join_pagination

		fillRightNav(request,context)
		if request.htmx:
			return render(request, "account/snippets/partial_post_list.html", context)

		return render(request, "account/account_profile.html", context)

class load_blog_this_user(LoginRequiredMixin, View):
	def get(self, request, user_id, *args, **kwargs):
		context = {}
		user = Account.objects.get(pk=user_id)
		blogs = Blog.objects.filter(author=user)
		context["blogs"] = blogs
		context["user"] = user
		
		return render(request, 'account/snippets/account_list_blog.html', context)

class load_qask_this_user(LoginRequiredMixin, View):
	def get(self, request, user_id, *args, **kwargs):
		context = {}
		user = Account.objects.get(pk=user_id)
		qasks = ForumPost.objects.filter(author=user)
		context["results"] = qasks
		context["user"] = user
		return render(request, 'account/snippets/account_list_qask.html', context)

class load_qrep_this_user(LoginRequiredMixin, View):
	def get(self, request, user_id, *args, **kwargs):
		context = {}
		user = Account.objects.get(pk=user_id)
		qreps = ForumReply.objects.filter(author=user)
		context["results"] = qreps
		context["user"] = user
		return render(request, 'account/snippets/account_list_qrep.html', context)

class load_post_this_user(LoginRequiredMixin, View):
	def get(self, request, user_id, *args, **kwargs):
		context = {}
		user = Account.objects.get(pk=user_id)
		posts   = Post.objects.filter(author=user).order_by('-created_on')
		context["results"] = posts
		context["user"] = user
		return render(request, 'account/snippets/account_list_post.html', context)

class load_like_this_user(LoginRequiredMixin, View):
	def get(self, request, user_id, *args, **kwargs):
		context = {}
		user = Account.objects.get(pk=user_id)
		posts   = Post.objects.filter(likes__in = [user.id]).order_by('-created_on')
		context["results"] = posts
		context["this_user"] = user
		return render(request, 'account/snippets/account_list_likes.html', context)

def load_qask_header(request, *args, **kwargs):
	user_id = kwargs.get("user_id")
	account = Account.objects.get(pk=user_id)
	return render(request, 'account/snippets/qask_nav.html', {"account":account})

def load_qrep_header(request, *args, **kwargs):
	user_id = kwargs.get("user_id")
	account = Account.objects.get(pk=user_id)
	return render(request, 'account/snippets/qrep_nav.html', {"account":account})

def load_blog_header(request, *args, **kwargs):
	user_id = kwargs.get("user_id")
	account = Account.objects.get(pk=user_id)
	return render(request, 'account/snippets/blog_nav.html', {"account":account})

def load_like_header(request, *args, **kwargs):
	user_id = kwargs.get("user_id")
	account = Account.objects.get(pk=user_id)
	return render(request, 'account/snippets/like_nav.html', {"account":account})

def load_post_header(request, *args, **kwargs):
	user_id = kwargs.get("user_id")
	account = Account.objects.get(pk=user_id)
	return render(request, 'account/snippets/post_nav.html', {"account":account})

@login_required
def account_search_view(request, *args, **kwargs):
	print("View")
	context = {}
	if request.method == "GET":
		
		search_query = request.GET.get("q")
		if len(search_query) > 0:
			search_username = Account.objects.filter(Q(username__icontains=search_query) | Q(profile__fullname__icontains=search_query)).distinct()
			
			context["results"] = search_username
				
	fillRightNav(request,context)
	return render(request, 'account/search_results.html', context)

@login_required
def edit_account_view(request, *args, **kwargs):
	if not request.user.is_authenticated:
		return redirect("login")
	user_id = kwargs.get("user_id")
	account = Account.objects.get(pk=user_id)
	profile = UserProfile.objects.get(account=account)

	if account.pk != request.user.pk:
		return HttpResponse("You cannot edit someone elses profile.")
	context = {}
	if request.POST and 'btn-account' in request.POST:
		form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
		
		if form.is_valid():
			#account.profile_image.delete()
			form.save()
			new_username = form.cleaned_data['username']
			return redirect("account:view", user_id=account.pk)
		else:
			form = AccountUpdateForm(request.POST, instance=request.user,
				initial={
					"id": account.pk,
					"email": account.email, 
					"username": account.username,
					"profile_image": account.profile_image,
					#"hide_email": account.hide_email,
				}
			)
			context['form'] = form

			context['profile'] = profile

	elif request.POST and 'btn-profile' in request.POST:
		form = ProfileUpdateForm(request.POST, instance=profile)
		print(form.errors)
		if form.is_valid():
			form.save()

			return redirect("account:view", user_id=account.pk)
	else:
		form = AccountUpdateForm(
			initial={
					"id": account.pk,
					"email": account.email, 
					"username": account.username,
					"profile_image": account.profile_image,
					"hide_email": account.hide_email,
				}
			)
		context['form'] = form

		context['profile'] = profile
		context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
	context["occupations"] = Occupation.objects.all()
	context["prodis"] = Prodi.objects.all()
	fillRightNav(request,context)
	return render(request, "account/edit_account_backup.html", context)

def save_temp_profile_image_from_base64String(imageString, user):
	INCORRECT_PADDING_EXCEPTION = "Incorrect padding"
	try:
		if not os.path.exists(settings.TEMP):
			os.mkdir(settings.TEMP)
		if not os.path.exists(settings.TEMP + "/" + str(user.pk)):
			os.mkdir(settings.TEMP + "/" + str(user.pk))
		url = os.path.join(settings.TEMP + "/" + str(user.pk),TEMP_PROFILE_IMAGE_NAME)
		storage = FileSystemStorage(location=url)
		image = base64.b64decode(imageString)
		with storage.open('', 'wb+') as destination:
			destination.write(image)
			destination.close()
		return url
	except Exception as e:
		print("exception: " + str(e))
		# workaround for an issue I found
		if str(e) == INCORRECT_PADDING_EXCEPTION:
			imageString += "=" * ((4 - len(imageString) % 4) % 4)
			return save_temp_profile_image_from_base64String(imageString, user)
	return None


def crop_image(request, *args, **kwargs):
	payload = {}
	user = request.user
	if request.POST and user.is_authenticated:
		try:
			imageString = request.POST.get("image")
			url = save_temp_profile_image_from_base64String(imageString, user)
			img = cv2.imread(url)

			cropX = int(float(str(request.POST.get("cropX"))))
			cropY = int(float(str(request.POST.get("cropY"))))
			cropWidth = int(float(str(request.POST.get("cropWidth"))))
			cropHeight = int(float(str(request.POST.get("cropHeight"))))
			if cropX < 0:
				cropX = 0
			if cropY < 0: # There is a bug with cropperjs. y can be negative.
				cropY = 0
			crop_img = img[cropY:cropY+cropHeight, cropX:cropX+cropWidth]

			cv2.imwrite(url, crop_img)

			# delete the old image
			#user.profile_image.delete() #problem with IAM permission

			# Save the cropped image to user model
			user.profile_image.save("profile_image.png", files.File(open(url, 'rb')))
			user.save()

			payload['result'] = "success"
			payload['cropped_profile_image'] = user.profile_image.url

			# delete temp file
			os.remove(url)

		except Exception as e:
			print("exception: " + str(e))
			payload['result'] = "error"
			payload['exception'] = str(e)
	return HttpResponse(json.dumps(payload), content_type="application/json")


