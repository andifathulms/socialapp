from .views import home, postdetail, AddReadList, AddClaps

from django.urls import path

app_name = 'blog'

urlpatterns = [
	path('', home, name='blog-home'),
	path('<int:id>/',postdetail, name='blog-detail' ),
	path('<int:pk>/read-list', AddReadList.as_view(), name='blog-readlist'),
	path('<int:pk>/claps', AddClaps.as_view(), name='blog-claps'),
]