from .views import home, postdetail, AddReadList, AddClaps, ReadingList

from django.urls import path

app_name = 'blog'

urlpatterns = [
	path('', home, name='blog-home'),
	path('read-list', ReadingList.as_view(), name='blog-readlist'),
	path('<int:id>/',postdetail, name='blog-detail' ),
	path('<int:pk>/read-list', AddReadList.as_view(), name='blog-readlist'),
	path('<int:pk>/claps', AddClaps.as_view(), name='blog-claps'),
]