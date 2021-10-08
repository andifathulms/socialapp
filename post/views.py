from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.utils import timezone

from .models import Post, Comment, Image
from .forms import PostForm, CommentForm, ShareForm

DEBUG = False

class PostListView(LoginRequiredMixin, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'
	def get(self, request, *args, **kwargs):
		logged_in_user = request.user

		posts = Post.objects.filter(
            author__userfollow__followers__in=[logged_in_user.id] #Fix later
        )
		form = PostForm(request.POST, request.FILES)
		share_form = ShareForm()

		context = {
			'post_list': posts,
			'shareform': share_form,
			'form': form,
		}
		context['debug_mode'] = settings.DEBUG
		context['debug'] = DEBUG
		context['room_id'] = "1"

		return render(request, 'post/post_list.html', context)
		#return render(request, 'layout-blank.html', context)

	def post(self, request, *args, **kwargs):
		logged_in_user = request.user
		
		posts = Post.objects.all().order_by('-created_on') #Fix later
		form = PostForm(request.POST, request.FILES)
		files = request.FILES.getlist('image')
		share_form = ShareForm()

		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.author = request.user
			new_post.save()

			for f in files:
				img = Image(image=f)
				img.save()
				new_post.image.add(img)

			new_post.save()

		context = {
			'post_list': posts,
			'shareform': share_form,
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

class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddCommentLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            comment.dislikes.remove(request.user)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            comment.likes.add(request.user)

        if is_like:
            comment.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddCommentDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            comment.likes.remove(request.user)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            comment.dislikes.add(request.user)

        if is_dislike:
            comment.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class CommentReplyView(LoginRequiredMixin, View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        post = Post.objects.get(pk=post_pk)
        parent_comment = Comment.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.save()

        return redirect('post:post-detail', pk=post_pk)

class SharedPostView(View):
    def post(self, request, pk, *args, **kwargs):
       original_post = Post.objects.get(pk=pk)
       form = ShareForm(request.POST)

       if form.is_valid():
            new_post = Post(
                shared_body=self.request.POST.get('body'),
                body=original_post.body,
                author=original_post.author,
                created_on=original_post.created_on,
                shared_user=request.user,
                shared_on=timezone.now(),
            )
            new_post.save()

            for img in original_post.image.all():
                new_post.image.add(img)

            new_post.save()

       return redirect('home')