from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie, requires_csrf_token
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView

from .models import Blog
from .forms import BlogForm

def home(request):
    if request.method=="POST":
        form=BlogForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.author = request.user
            post=form.save()
            messages.success(request,'submitted succesfully {}'.format(post))
            return redirect('/')      
    form=BlogForm()
    return render(request,'blog/blog_form.html',{'form':form})

def postdetail(request,id):
    post=Blog.objects.get(id=id)
    return render(request,'blog/blog_detail.html',{'post':post})

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
