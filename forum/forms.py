from django import forms
from .models import ForumPost, ForumReply

class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['title', 'body']

class ForumReplyForm(forms.ModelForm):
    class Meta:
        model = ForumReply
        fields = ['reply']