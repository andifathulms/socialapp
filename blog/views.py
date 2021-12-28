from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie, requires_csrf_token
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponseRedirect

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.contrib import messages
from django.views.generic import ListView, UpdateView, DeleteView

import json
import re

from .models import Blog
from .forms import BlogForm



CLEANR = re.compile('<.*?>')

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

def home(request):
    if request.method=="POST":
        form=BlogForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.author = request.user

            if 'draft' in request.POST:
                post.is_draft = True
            
            post=form.save()
            
            messages.success(request,'submitted succesfully {}'.format(post))
            return redirect('/')
            #redirect('blog:blog-manage')   
    form = BlogForm()
    context = {'form':form}
    fillRightNav(request, context)
    return render(request,'blog/blog_form.html',context)

def postdetail(request,id):
    post=Blog.objects.get(id=id)
    context = {'post':post}

    fillRightNav(request,context)

    return render(request,'blog/blog_detail.html',context)


class ReadingList(ListView):
    def get(self, request, *args, **kwargs):
        
        readlist = Blog.objects.filter(read_list__in=[request.user.id], is_draft=False)

        page = request.GET.get('page', 1)
        join_paginator = Paginator(readlist,10)
        
        try:
            join_pagination = join_paginator.page(page)
        except PageNotAnInteger:
            join_pagination = join_paginator.page(1)
        except EmptyPage:
            join_pagination = join_paginator.page(join_paginator.num_pages)

        context = {
            'results' : join_pagination,
        }

        
        fillRightNav(request, context)

        return render(request, 'blog/reading_list.html', context)

class BlogUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    fields = ['title', 'body']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class BlogDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    success_url ="/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class ManageBlog(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        published_posts = Blog.objects.filter(author=request.user, is_draft=False)
        drafted_posts = Blog.objects.filter(author=request.user, is_draft=True)

        context["published_posts"] = published_posts
        context["drafted_posts"] = drafted_posts

        fillRightNav(request, context)

        return render(request, 'blog/blog_manage.html', context)

    def post(self, request, pk, *args, **kwargs):
        context = {}
        published_posts = Blog.objects.filter(author=request.user, is_draft=False)
        drafted_posts = Blog.objects.filter(author=request.user, is_draft=True)

        context["published_posts"] = published_posts
        context["drafted_posts"] = drafted_posts

        fillRightNav(request, context)

        if 'publish' in request.POST:
            blog = Blog.objects.get(pk=pk)
            blog.is_draft = False
            blog.save()

            return redirect('blog:blog-manage')

        if 'draft' in request.POST:
            blog = Blog.objects.get(pk=pk)
            blog.is_draft = True
            blog.save()

            return redirect('blog:blog-manage')

        return render(request, 'blog/blog_manage.html', context)

class AddReadList(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        blog = Blog.objects.get(pk=pk)

        is_readlist = False

        for user in blog.read_list.all():
            if user == request.user:
                is_readlist = True
                break

        if not is_readlist:
            blog.read_list.add(request.user)

        if is_readlist:
            blog.read_list.remove(request.user)
            
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddClaps(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        blog = Blog.objects.get(pk=pk)

        is_claps = False

        for user in blog.claps.all():
            if user == request.user:
                is_claps = True
                break

        if not is_claps:
            blog.claps.add(request.user)

        if is_claps:
            blog.claps.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


@requires_csrf_token
def uploadi(request):
    f=request.FILES['image']
    fs=FileSystemStorage()
    filename=str(f).split('.')[0]
    file= fs.save(filename,f)
    fileurl=fs.url(file)
    return JsonResponse({'success':1,'file':{'url':fileurl}})

@requires_csrf_token
def uploadf(request):
        f=request.FILES['file']
        fs=FileSystemStorage()
        filename,ext=str(f).split('.')
        print(filename,ext)
        file=fs.save(str(f),f)
        fileurl=fs.url(file)
        fileSize=fs.size(file)
        return JsonResponse({'success':1,'file':{'url':fileurl,'name':str(f),'size':fileSize}})


def upload_link_view(request):
    import requests
    from bs4 import BeautifulSoup  

    print(request.GET['url'])
    url = request.GET['url']
    response = requests.get(url)
    soup = BeautifulSoup(response.text,features="html.parser")
    metas = soup.find_all('meta')
    description=""
    title=""
    image=""
    for meta in metas:
        if 'property' in meta.attrs:
            if (meta.attrs['property']=='og:image'):
                image=meta.attrs['content']         
        elif 'name' in meta.attrs:         
            if (meta.attrs['name']=='description'):
                description=meta.attrs['content']
            if (meta.attrs['name']=='title'):
                title=meta.attrs['content']
    return JsonResponse({'success':1,'meta':
    {"description":description,"title":title, "image":{"url":image}
        }})

class load_blog_preview(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        context = {}
        blog = Blog.objects.get(pk=pk)
        text = blog.body

        #find read time
        words = len(text.split())
        time = words//225

        #find the image and text
        body = json.loads(text)
        blocks = body["blocks"]
        textBody = ""
        imgFlag = False
        image = ""

        for block in blocks:
            if block["type"] == "paragraph":
                textBody += block["data"]["text"]

            if block["type"] == "Image":
                if not imgFlag:
                    image = block["data"]["file"]["url"];
                    imgFlag = True

        context["time"] = time
        context["text"] = cleanhtml(truncateString(textBody, 180))
        context["image"] = image
        context["imgFlag"] = imgFlag
        context["title"] = blog.title
        context["pk"] = pk

        return render(request, 'blog/snippets/blog_preview_body.html', context)

class load_blog_span_preview(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        context = {}
        blog = Blog.objects.get(pk=pk)
        text = blog.body

        #find read time
        words = len(text.split())
        time = words//225

        context["time"] = time
        context["pk"] = pk
        context["date"] = blog.created_on

        return render(request, 'blog/snippets/blog_span_sidebar.html', context)


def truncateString(str, num):
    if len(str) <= num:
        return str
    return str[0:num] + '...'
