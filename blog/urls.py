from .views import home, postdetail, AddReadList, AddClaps, ReadingList, ManageBlog, BlogUpdate, BlogDelete, load_blog_preview, load_blog_span_preview

from django.urls import path

app_name = 'blog'

urlpatterns = [
	path('', home, name='blog-home'),
	path('read-list', ReadingList.as_view(), name='blog-readlist'),
	path('manage-blog', ManageBlog.as_view(), name='blog-manage'),
	path('manage-blog/<int:pk>', ManageBlog.as_view(), name='blog-action'),
	path('update/<int:pk>', BlogUpdate.as_view(), name='blog-update'),
	path('delete/<int:pk>', BlogDelete.as_view(), name='blog-delete'),
	path('<int:id>/',postdetail, name='blog-detail' ),
	path('<int:pk>/read-list', AddReadList.as_view(), name='blog-readlist'),
	path('<int:pk>/claps', AddClaps.as_view(), name='blog-claps'),
	path('load-blog-preview/<int:pk>',load_blog_preview.as_view(), name='load-blog-preview'),
	path('load-blog-span-sidebar/<int:pk>',load_blog_span_preview.as_view(), name='load-blog-span-sidebar'),
]