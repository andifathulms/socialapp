from django.urls import path

from account.views import(
	account_view,
	edit_account_view,
	crop_image,
	load_blog_this_user,
	load_qask_this_user,
	load_post_this_user,
	load_qrep_this_user,
	load_like_this_user,
	load_qask_header,
	load_post_header,
	load_blog_header,
	load_like_header,
	load_qrep_header,
) 

app_name = 'account'

urlpatterns = [
	path('<user_id>/', account_view, name="view"),
	path('<user_id>/edit/', edit_account_view, name="edit"),
	path('<user_id>/edit/cropImage/', crop_image, name="crop_image"),

	path('load-blog-this-user/<user_id>/', load_blog_this_user.as_view(), name="load-blog-this-user"),
	path('load-qask-this-user/<user_id>/', load_qask_this_user.as_view(), name="load-qask-this-user"),
	path('load-post-this-user/<user_id>/', load_post_this_user.as_view(), name="load-post-this-user"),
	path('load-qrep-this-user/<user_id>/', load_qrep_this_user.as_view(), name="load-qrep-this-user"),
	path('load-like-this-user/<user_id>/', load_like_this_user.as_view(), name="load-like-this-user"),

	path('load-qask-header/<user_id>/', load_qask_header, name="load-qask-header"),
	path('load-post-header/<user_id>/', load_post_header, name="load-post-header"),
	path('load-blog-header/<user_id>/', load_blog_header, name="load-blog-header"),
	path('load-like-header/<user_id>/', load_like_header, name="load-like-header"),
	path('load-qrep-header/<user_id>/', load_qrep_header, name="load-qrep-header"),
]