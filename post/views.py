from django.shortcuts import render
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView

from .models import Post, Comment
from .forms import PostForm, CommentForm

DEBUG = False

class PostListView(LoginRequiredMixin, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'
	def get(self, request, *args, **kwargs):
		logged_in_user = request.user

		posts = Post.objects.all().order_by('-created_on')
		form = PostForm()

		context = {
			'post_list': posts,
			'form': form,
		}
		context['debug_mode'] = settings.DEBUG
		context['debug'] = DEBUG
		context['room_id'] = "1"

		return render(request, 'post/post_list.html', context)
		#return render(request, 'layout-blank.html', context)

	def post(self, request, *args, **kwargs):
		logged_in_user = request.user
		
		posts = Post.objects.all().order_by('-created_on')
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.author = request.user
			new_post.save()

		context = {
			'post_list': posts,
			'form': form,
		}
		context['debug_mode'] = settings.DEBUG
		context['debug'] = DEBUG
		context['room_id'] = "1"
		
		return render(request, 'post/post_list.html', context)

class PostDetailView(LoginRequiredMixin, View):
	def get(self, request, pk, *args, **kwargs):
		post = Post.objects.get(pk=pk)
		form = CommentForm()
		comments = Comment.objects.filter(post=post).order_by('-created_on')

		context = {
			'post': post,
			'form': form,
			'comments': comments,
		}        
		return render(request, 'post/post_detail.html', context)
	def post(self, request, pk, *args, **kwargs):
		post = Post.objects.get(pk=pk)
		form = CommentForm(request.POST)

		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.author = request.user
			new_comment.post = post
			new_comment.save()

		comments = Comment.objects.filter(post=post).order_by('-created_on')

		context = {
			'post': post,
			'form': form,
			'comments': comments,
		}

		return render(request, 'post/post_detail.html', context)

class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['body']
	template_name = 'post/post_edit.html'

	def get_success_url(self):
		pk = self.kwargs['pk']
		return reverse_lazy('post:post-detail', kwargs={'pk': pk})

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	template_name = 'post/post_delete.html'
	success_url = reverse_lazy('home')

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Comment
	template_name = 'post/comment_delete.html'

	def get_success_url(self):
		pk = self.kwargs['post_pk']
		return reverse_lazy('post:post-detail', kwargs={'pk': pk})

	def test_func(self):
		comment = self.get_object()
		return self.request.user == comment.author