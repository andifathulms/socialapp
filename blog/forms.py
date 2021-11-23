from django import forms
from .views import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model=Blog
        fields=['title','body']