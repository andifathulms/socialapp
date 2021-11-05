from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.settings import api_settings

from.serializers import PostSerializer, CommentSerializer
from post.models import Post, Comment

from django.db.models import F
from django.shortcuts import render, redirect
from django.urls import reverse_lazy


class PostAPIList(APIView):
    permission_classes = (AllowAny,)
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def get(self, request, format=None):
        post = Post.objects.all()
        page = self.paginate_queryset(post)
        serializer = PostSerializer(post, many=True)

        return self.get_paginated_response(serializer.data)
  
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
         """
         Return a single page of results, or `None` if pagination is disabled.
         """
         if self.paginator is None:
             return None
         return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
         """
         Return a paginated style `Response` object for the given output data.
         """
         assert self.paginator is not None
         return self.paginator.get_paginated_response(data) 

class PostAPIDetail(APIView):
    permission_classes = (AllowAny,)
    """
    Retrieve, update or delete a transformer instance
    """
    def get_object(self, pk):
        # Returns an object instance that should 
        # be used for detail views.
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
  
    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        context = {
            'post': post
        }
        serializer = PostSerializer(post)

        return render(request, 'post/snippets/post_detail_tweet.html', context)
        #return Response(serializer.data)
  
    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        context = {
            'post': post
        }
        if serializer.is_valid():
            serializer.save()

            return render(request, 'post/snippets/post_detail_tweet.html', context)
            #return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
    def patch(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post,
                                           data=request.data,
                                           partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
  
    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentAPIDetail(APIView):
    permission_classes = (AllowAny,)
    """
    Retrieve, update or delete a transformer instance
    """
    def get_object(self, pk):
        # Returns an object instance that should 
        # be used for detail views.
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404
  
    def get(self, request, post_pk, pk, format=None):
        comment = self.get_object(pk)
        post = Post.objects.get(pk=post_pk)
        context = {
            'comment': comment,
            'post' : post
        }
        serializer = CommentSerializer(comment)

        return render(request, 'post/snippets/post_detail_edited_comment.html', context)
        #return Response(serializer.data)
  
    def put(self, request, post_pk, pk, format=None):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment, data=request.data)
        post = Post.objects.get(pk=post_pk)
        context = {
            'comment': comment,
            'post' : post
        }
        if serializer.is_valid():
            serializer.save()

            return render(request, 'post/snippets/post_detail_edited_comment.html', context)
            #return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
    def patch(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post,
                                           data=request.data,
                                           partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
  
    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)