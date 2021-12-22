from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponseRedirect
from django.db.models import F, Sum, Count

from chat.utils import calculate_timestamp

from .models import Subject, ForumPost, ForumReply
from account_profile.models import UserProfile
from .forms import ForumPostForm, ForumReplyForm

from blog.models import Blog

def fillRightNav(request,context):
    subject = Subject.objects.filter(subscriber__in=[request.user.id])
    forum = ForumPost.objects.filter(subject__in=subject).order_by('-created_on')[:4]
    forump = ForumPost.objects.annotate(count=Count('forumpost_parent')).order_by('-count')[:4]
    
    context["forum_newest"] = forum
    context["forum_popular"] = forump
    context["type"] = "forum"

class SubjectListView(LoginRequiredMixin, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def get(self, request, *args, **kwargs):
		logged_in_user = request.user
		context = {}
		
		general_subject = Subject.objects.filter(type='General')
		faculty_subject = Subject.objects.filter(type='Faculty')

		gen_container = []
		for subject in general_subject:
			count = ForumPost.objects.filter(subject=subject).aggregate(Sum('view'))
			total = ForumPost.objects.filter(subject=subject).count()
			print(count)
			gen_container.append((subject,total,count['view__sum']))

		fac_container = []
		for subject in faculty_subject:
			count = ForumPost.objects.filter(subject=subject).aggregate(Sum('view'))
			total = ForumPost.objects.filter(subject=subject).count()

			fac_container.append((subject,total,count['view__sum']))

		context['general_subject'] = gen_container
		context['faculty_subject'] = fac_container
		fillRightNav(request,context)
		return render(request, 'forum/forum_home.html', context)

class ForumListView(LoginRequiredMixin, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def get(self, request, pk, *args, **kwargs):
		logged_in_user = request.user
		context = {}

		subject = Subject.objects.get(pk=pk)
		post = ForumPost.objects.filter(subject=subject).order_by('-created_on')
		
		is_upvote = False
		is_downvote = False
		p_list = []
		for p in post:
			reply = ForumReply.objects.filter(post=p).count()

			for upvote in p.upvote.all():
				if upvote == logged_in_user:
					is_upvote = True
					break

			for downvote in p.downvote.all():
				if downvote == logged_in_user:
					is_downvote = True
					break

			p_list.append((p,reply,is_upvote,is_downvote))
			is_upvote = False
			is_downvote = False

		context["subject"] = subject
		context["posts"] = p_list
		fillRightNav(request,context)

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
		
		is_upvote = False
		is_downvote = False
		p_list = []
		for p in post:
			reply = ForumReply.objects.filter(post=p).count()
			
			for upvote in p.upvote.all():
				if upvote == logged_in_user:
					is_upvote = True
					break

			for downvote in p.downvote.all():
				if downvote == logged_in_user:
					is_downvote = True
					break

			p_list.append((p,reply,is_upvote,is_downvote))
			is_upvote = False
			is_downvote = False

		context["subject"] = subject
		context["posts"] = p_list
		fillRightNav(request,context)
		return render(request, 'forum/forum_content.html', context)

class ForumDetailView(LoginRequiredMixin, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def get(self, request, pk, *args, **kwargs):
		logged_in_user = request.user
		context = {}

		post = ForumPost.objects.get(pk=pk)
		user_profile = UserProfile.objects.get(account=logged_in_user)
		post_reply = ForumReply.objects.filter(post=post)
		subject = post.subject
		
		counter = ForumPost.objects.get(id = pk)
		counter.view = F('view')+1
		counter.save(update_fields=["view"])


		context["subject"] = subject
		context["post"] = post
		context["user_profile"] = user_profile
		#context["replies"] = reply_list
		context["replies"] = post_reply
		fillRightNav(request,context)
		#print("render")
		return render(request, 'forum/forum_detail_2.html', context)

	def post(self, request, pk, parent_comment_id=None, *args, **kwargs):
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

			#If secondary response
			if parent_comment_id:
				parent_comment = ForumReply.objects.get(id=parent_comment_id)
				forum_reply.parent_id = parent_comment.id
				#Respondent
				forum_reply.reply_to = parent_comment.author
				forum_reply.save()
				#return HttpResponse('200 OK')
				#return render(request, 'forum/forum_detail_2.html', context)

			forum_reply.save()
		else:
			print(request.POST)
			print(form.errors)

		post_reply = ForumReply.objects.filter(post=post)

		context["subject"] = subject
		context["post"] = post
		#context["replies"] = reply_list
		context["replies"] = post_reply
		fillRightNav(request,context)
		return render(request, 'forum/forum_detail_2.html', context)
		#return render(request, 'forum/snippets/forum_detail/comments.html', context)

class AddUpvote(LoginRequiredMixin, View):

	def post(self, request, pk, *args, **kwargs):
		forum_post = ForumPost.objects.get(pk=pk)

		is_downvote = False

		for downvote in forum_post.downvote.all():
			if downvote == request.user:
				is_downvote = True
				break

		if is_downvote:
			forum_post.downvote.remove(request.user)

		is_upvote = False

		for upvote in forum_post.upvote.all():
			if upvote == request.user:
				is_upvote = True
				break

		if not is_upvote:
			forum_post.upvote.add(request.user)

		if is_upvote:
			forum_post.upvote.remove(request.user)

		next = request.POST.get('next', '/')
		return HttpResponseRedirect(next)

class AddDownvote(LoginRequiredMixin, View):

	def post(self, request, pk, *args, **kwargs):
		forum_post = ForumPost.objects.get(pk=pk)

		is_upvote = False

		for upvote in forum_post.upvote.all():
			if upvote == request.user:
				is_upvote = True
				break

		if is_upvote:
			forum_post.upvote.remove(request.user)

		is_downvote = False

		for downvote in forum_post.downvote.all():
			if downvote == request.user:
				is_downvote = True
				break

		if not is_downvote:
			forum_post.downvote.add(request.user)

		if is_downvote:
			forum_post.downvote.remove(request.user)

		next = request.POST.get('next', '/')
		return HttpResponseRedirect(next)

class AddReplyUpvote(LoginRequiredMixin, View):

	def post(self, request, pk, *args, **kwargs):
		forum_post = ForumReply.objects.get(pk=pk)

		is_downvote = False

		for downvote in forum_post.downvote.all():
			if downvote == request.user:
				is_downvote = True
				break

		if is_downvote:
			forum_post.downvote.remove(request.user)

		is_upvote = False

		for upvote in forum_post.upvote.all():
			if upvote == request.user:
				is_upvote = True
				break

		if not is_upvote:
			forum_post.upvote.add(request.user)

		if is_upvote:
			forum_post.upvote.remove(request.user)

		next = request.POST.get('next', '/')
		return HttpResponseRedirect(next)

class AddReplyDownvote(LoginRequiredMixin, View):

	def post(self, request, pk, *args, **kwargs):
		forum_post = ForumReply.objects.get(pk=pk)

		is_upvote = False

		for upvote in forum_post.upvote.all():
			if upvote == request.user:
				is_upvote = True
				break

		if is_upvote:
			forum_post.upvote.remove(request.user)

		is_downvote = False

		for downvote in forum_post.downvote.all():
			if downvote == request.user:
				is_downvote = True
				break

		if not is_downvote:
			forum_post.downvote.add(request.user)

		if is_downvote:
			forum_post.downvote.remove(request.user)

		next = request.POST.get('next', '/')
		return HttpResponseRedirect(next)

class AddSubscribe(LoginRequiredMixin, View):

	def post(self, request, pk, *args, **kwargs):
		subject = Subject.objects.get(pk=pk)

		if request.user in subject.subscriber.all():
			subject.subscriber.remove(request.user)
		else:
			subject.subscriber.add(request.user)

		next = request.POST.get('next', '/')
		return HttpResponseRedirect(next)

class UpvoteForumPostList(LoginRequiredMixin, View):

	def post(self, request, pk, *args, **kwargs):
		context = {}
		forum_post = ForumPost.objects.get(pk=pk)

		is_upvote = False
		is_downvote = False

		if request.user in forum_post.upvote.all():
			is_upvote = True

		if is_upvote:
			forum_post.upvote.remove(request.user)
			is_upvote = False
		else:
			forum_post.upvote.add(request.user)
			is_upvote = True
			
		if request.user in forum_post.downvote.all():
			is_downvote = True

		if is_downvote:
			forum_post.downvote.remove(request.user)
			is_downvote = False

		context["is_upvote"] = is_upvote #this two is reversing, careful
		context["is_downvote"] = is_downvote
		context["upvote"] = forum_post.upvote.all().count 
		context["downvote"] = forum_post.downvote.all().count
		context["reply"] = forum_post.forumpost_parent.count
		context["pk"] = pk
		
		return render(request, 'forum/snippets/forum_count_post_list.html', context)

class DownvoteForumPostList(LoginRequiredMixin, View):

	def post(self, request, pk, *args, **kwargs):
		context = {}
		forum_post = ForumPost.objects.get(pk=pk)

		is_downvote = False
		is_upvote = False

		if request.user in forum_post.downvote.all():
			is_downvote = True

		if is_downvote:
			forum_post.downvote.remove(request.user)
			is_downvote = False
		else:
			forum_post.downvote.add(request.user)
			is_downvote = True

		if request.user in forum_post.upvote.all():
			is_upvote = True

		if is_upvote:
			forum_post.upvote.remove(request.user)
			is_upvote = False

		context["is_upvote"] = is_upvote #this two is reversing, careful
		context["is_downvote"] = is_downvote
		context["upvote"] = forum_post.upvote.all().count 
		context["downvote"] = forum_post.downvote.all().count
		context["reply"] = forum_post.forumpost_parent.count
		context["pk"] = pk
		
		return render(request, 'forum/snippets/forum_count_post_list.html', context)

class ChangeRightNav1(LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		context = {}

		subject = Subject.objects.filter(subscriber__in=[request.user.id])
		forump = ForumPost.objects.annotate(count=Count('forumpost_parent')).order_by('-count')[:5]
		context["forum_popular"] = forump
		return render(request, 'snippets/right-sidebar-test-1.html', context)

class ChangeRightNav2(LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		context = {}

		subject = Subject.objects.filter(subscriber__in=[request.user.id])
		forum = ForumPost.objects.filter(subject__in=subject).order_by('-created_on')[:5]
		context["forum_newest"] = forum
		return render(request, 'snippets/right-sidebar-test-2.html', context)

### MASSIVE OFFSIDE BY A MARGIN ###
class ChangeRightNav0(LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		context = {}
		readlist = Blog.objects.filter(read_list__in=[request.user.id], is_draft=False)[:4]
		count = Blog.objects.filter(read_list__in=[request.user.id], is_draft=False).count()

		context["readlist"] = readlist
		context["readlist_count"] = count
		return render(request, 'snippets/right-sidebar.html', context)