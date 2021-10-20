from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from django.db.models import F

from chat.utils import calculate_timestamp

from .models import Subject, ForumPost, ForumReply
from account_profile.models import UserProfile
from .forms import ForumPostForm, ForumReplyForm

class SubjectListView(LoginRequiredMixin, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def get(self, request, *args, **kwargs):
		logged_in_user = request.user
		context = {}

		general_subject = Subject.objects.filter(type='General')
		faculty_subject = Subject.objects.filter(type='Faculty')

		context['general_subject'] = general_subject
		context['faculty_subject'] = faculty_subject

		return render(request, 'forum/forum_home.html', context)

class ForumListView(LoginRequiredMixin, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def get(self, request, pk, *args, **kwargs):
		logged_in_user = request.user
		context = {}

		subject = Subject.objects.get(pk=pk)
		post = ForumPost.objects.filter(subject=subject).order_by('-created_on')
		
		p_list = []
		for p in post:
			reply = ForumReply.objects.filter(post=p).count()
			p_list.append((p,reply))

		context["subject"] = subject
		context["posts"] = p_list
		print(p_list)

		return render(request, 'forum/forum_content.html', context)

	def post(self, request, pk, *args, **kwargs):
		logged_in_user = request.user
		context = {}

		subject = Subject.objects.get(pk=pk)
		form = ForumPostForm(request.POST)

		if form.is_valid():
			forum_post = form.save(commit=False)
			forum_post.subject = subject
			forum_post.author = logged_in_user
			forum_post.save()
		else:
			print(request.POST)
			print(form.errors)

		post = ForumPost.objects.filter(subject=subject).order_by('-created_on')
		p_list = []
		for p in post:
			reply = ForumReply.objects.filter(post=p).count()
			p_list.append((p,reply))

		context["subject"] = subject
		context["posts"] = p_list

		return render(request, 'forum/forum_content.html', context)

class ForumDetailView(LoginRequiredMixin, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def get(self, request, pk, *args, **kwargs):
		logged_in_user = request.user
		context = {}

		post = ForumPost.objects.get(pk=pk)
		user_profile = UserProfile.objects.get(account=logged_in_user)
		post_reply = ForumReply.objects.filter(post=post).order_by('-created_on')
		subject = post.subject
		
		#print(post.view)
		counter = ForumPost.objects.get(id = pk)
		counter.view = F('view')+0.5
		counter.save(update_fields=["view"])
		#post = ForumPost.objects.get(pk=pk)
		#print(post.view)

		reply_list = []
		for reply in post_reply:
			profile = UserProfile.objects.get(account=reply.author)
			timestamp = calculate_timestamp(reply.created_on)

			reply_list.append((reply,profile,timestamp))

		context["subject"] = subject
		context["post"] = post
		context["user_profile"] = user_profile
		context["timestamp"] = calculate_timestamp(post.created_on)
		context["replies"] = reply_list

		#print("render")
		return render(request, 'forum/forum_detail.html', context)

	def post(self, request, pk, *args, **kwargs):
		logged_in_user = request.user
		context = {}

		post = ForumPost.objects.get(pk=pk)
		user_profile = UserProfile.objects.get(account=logged_in_user)
		subject = post.subject

		form = ForumReplyForm(request.POST)

		if form.is_valid():
			forum_reply = form.save(commit=False)
			forum_reply.post = post
			forum_reply.author = logged_in_user
			forum_reply.save()
		else:
			print(request.POST)
			print(form.errors)

		post_reply = ForumReply.objects.filter(post=post).order_by('-created_on')
		reply_list = []
		for reply in post_reply:
			profile = UserProfile.objects.get(account=reply.author)
			timestamp = calculate_timestamp(reply.created_on)

			reply_list.append((reply,profile,timestamp))

		context["subject"] = subject
		context["post"] = post
		context["user_profile"] = user_profile
		context["timestamp"] = calculate_timestamp(post.created_on)
		context["replies"] = reply_list
		
		return render(request, 'forum/forum_detail.html', context)
