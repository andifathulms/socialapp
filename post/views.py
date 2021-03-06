from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post, Comment, Image, Tag
from .forms import PostForm, CommentForm, ShareForm, ExploreForm

from marketplace.models import Product
from forum.models import ForumPost, Subject
from blog.models import Blog

from itertools import chain
from operator import attrgetter

DEBUG = False

def fillRightNav(request,context):
    readlist = Blog.objects.filter(read_list__in=[request.user.id], is_draft=False)[:4]
    count = Blog.objects.filter(read_list__in=[request.user.id], is_draft=False).count()

    context["readlist"] = readlist
    context["readlist_count"] = count
    context["type"] = "blog"

class PostListView(LoginRequiredMixin, View):
    
    def postlist_populated(self, request, context):
        #posts = Post.objects.filter(author__userfollow__followers__in=[request.user.id])#Fix later #For reference
        posts = Post.objects.all().order_by('-created_on') #Fix later
        product = Product.objects.all()
        subject = Subject.objects.filter(subscriber__in=[request.user.id])
        forum = ForumPost.objects.filter(subject__in=subject)
        blog = Blog.objects.filter(is_draft=False) #Fix later
        result_list = sorted(chain(posts, product, forum, blog),key=attrgetter('created_on'), reverse=True)
        join_paginator = Paginator(result_list,10)
        page = request.GET.get('page', 1)
        
        try:
            join_pagination = join_paginator.page(page)
        except PageNotAnInteger:
            join_pagination = join_paginator.page(1)
        except EmptyPage:
            join_pagination = join_paginator.page(join_paginator.num_pages)

        context["results"] = join_pagination
        context["is_home"] = True

    def get(self, request, *args, **kwargs):
        
        context = {}

        fillRightNav(request, context)
        self.postlist_populated(request, context)

        if request.htmx:
            print(context["results"])
            return render(request, "post/snippets/post_list_body_2.html", context)

        return render(request, 'post/post_list_2.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = PostForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

            new_post.create_tags()

            for f in files:
                img = Image(image=f)
                img.save()
                new_post.image.add(img)

            new_post.save()
            
        else:
            print(form.errors)
        
        fillRightNav(request, context)
        self.postlist_populated(request, context)

        return render(request, 'post/snippets/post_list_body_2.html', context)

class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        comments = Comment.objects.filter(post=post).order_by('-created_on')
        
        is_post_like = False
        if request.user in post.likes.all():
            is_post_like = True

        comment_list = []
        for comment in comments:
            is_like = False
            if request.user in comment.likes.all():
                is_like = True

            comment_list.append((comment,is_like))

        '''
        page = request.GET.get('page', 1)
        paginator = Paginator(comment_list,7)

        try:
            comment_pagination = paginator.page(page)
        except PageNotAnInteger:
            comment_pagination = paginator.page(1)
        except EmptyPage:
            comment_pagination = paginator.page(paginator.num_pages)'''

        context = {
            'post': post,
            'result': post,
            'form': form,
            'comments': comment_list,
            'is_post_like' : is_post_like,
        } 
        fillRightNav(request, context)       
        return render(request, 'post/post_detail.html', context)
    def post(self, request, pk, *args, **kwargs):
        
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)
        files = request.FILES.getlist('image')

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

            new_comment.create_tags()

            for f in files:
                img = Image(image=f)
                img.save()
                new_comment.image.add(img)

            new_comment.save()
        else:
            print(form.errors)

        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }
        fillRightNav(request, context)
        print(context)
        return render(request, 'post/snippets/post_detail_new_comment.html', context)

#obsolete?
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

#edit with htmx?
class PostEditViewHTMX(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)


        context = {
            'post': post
        }

        return render(request, 'post/snippets/post_detail_inline_editing.html', context)
    def put(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = PostForm(request.PUT, request.FILES)
        files = request.FILES.getlist('image')

        if form.is_valid():
            print(request.PUT)

            post.create_tags()

            for f in files:
                img = Image(image=f)
                img.save()
                post.image.add(img)

            #post.save()
            
        else:
            print(form.errors)

        return render(request, 'post/post_detail_tweet.html', context)


class CommentEditViewHTMX(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    def get(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)
        post_pk = self.kwargs['post_pk']
        post = Post.objects.get(pk=post_pk)

        context = {
            'comment': comment,
            'post' : post,
        }

        return render(request, 'post/snippets/post_detail_inline_editing_comment.html', context)

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
        context = {}
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

        context["result"] = post
        return render(request,"post/snippets/like_post_button.html",context)

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
    def post(self, request, post_pk, pk, *args, **kwargs):
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

        post = Post.objects.get(pk=post_pk)
        context={}
        context["result"] = comment
        
        return render(request, 'post/snippets/comment_like.html', context)

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

class Explore(View):
    def get(self, request, *args, **kwargs):
        explore_form = ExploreForm()
        query = self.request.GET.get('query')
        tag = Tag.objects.filter(name=query).first()
        #print(tag.name)

        if tag:
            posts = Post.objects.filter(tags__in=[tag])
        else:
            posts = Post.objects.all()

        context = {
            'tag': tag,
            'posts': posts,
            'explore_form': explore_form,
        }

        #print(context['posts'])

        return render(request, 'post/explore.html', context)

    def post(self, request, *args, **kwargs):
        explore_form = ExploreForm(request.POST)
        if explore_form.is_valid():
            query = explore_form.cleaned_data['query']
            tag = Tag.objects.filter(name=query).first()

            posts = None
            if tag:
                posts = Post.objects.filter(tags__in=[tag])

            if posts:
                context = {
                    'tag': tag,
                    'posts': posts,
                }
            else:
                context = {
                    'tag': tag,
                }
            return HttpResponseRedirect(f'/explore?query={query}')
        return HttpResponseRedirect('/explore')

def populateURL(post, context):
    import requests
    from bs4 import BeautifulSoup

    url = post.url
    response = requests.get(url)
    soup = BeautifulSoup(response.text,features="html.parser")
    metas = soup.find_all('meta')

    description = ""
    title = ""
    image = ""
    site = ""
    for meta in metas:
        if 'property' in meta.attrs:
            #print(meta.attrs['property'])
            if(meta.attrs['property']=='og:image'):
                image=meta.attrs['content']
            if(meta.attrs['property']=='og:site_name'):
                site=meta.attrs['content']
        elif 'name' in meta.attrs:
            #print(meta.attrs['name'])
            if(meta.attrs['name']=='description'):
                description=meta.attrs['content']
            if(meta.attrs['name']=='title'):
                title=meta.attrs['content']

    context["description"] = description
    context["title"] = title
    context["image"] = image
    context["url"] = url
    context["site"] = site

class LoadUrlPreview(View):

    def get(self, request, pk, *args, **kwargs):
        import requests
        from bs4 import BeautifulSoup

        print("Fired from " + str(pk))

        context = {}

        post = Post.objects.get(pk=pk)
        url = post.url
        response = requests.get(url)
        soup = BeautifulSoup(response.text,features="html.parser")
        metas = soup.find_all('meta')
        
        description = ""
        title = ""
        image = ""
        site = ""
        for meta in metas:
            
            if 'property' in meta.attrs:
                #print(meta.attrs['property'])
                if(meta.attrs['property']=='og:image'):
                    image=meta.attrs['content']
                if(meta.attrs['property']=='og:site_name'):
                    site=meta.attrs['content']
            elif 'name' in meta.attrs:
                #print(meta.attrs['name'])
                if(meta.attrs['name']=='description'):
                    description=meta.attrs['content']
                if(meta.attrs['name']=='title'):
                    title=meta.attrs['content']

        context["description"] = description
        context["title"] = title
        context["image"] = image
        context["url"] = url
        context["site"] = site

        return render(request, 'post/snippets/load_url_preview.html', context)