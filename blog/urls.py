from .views import home, postdetail

from django.urls import path

app_name = 'blog'

urlpatterns = [
	path('', home, name='blog-home'),
	path('<int:id>/',postdetail ),
]