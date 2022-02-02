Framework/tools utama yang digunakan dalam pembuatan PNP Talk antara lain : Django sebagai Back End (Django 3.2.7), htmx untuk AJAX-related functioned (htmx is small ~10k, and dependency free), Django Channel sebagai ASGI layer pada Django, mengatur Web Sockets dan Chat Protocol, digunakan pada fitur Chatting dan Notifications. Untuk cache menggunakan channel_redis, dan Daphne sebagai HTTP server and WebSocket termination server.

Juga beberapa library berikut juga digunakan dalam project ini antara lain : boto3 untuk library penghubung ke AWS S3, beautifulsoup untuk web scraping (digunakan untuk scraping link yang masuk di post/tweet, untuk menghasilkan info seperti thumbnail, title, dll), django-mptt (MPTT : Modified Preorder Tree Traversal) digunakan di Forum untuk memudahkan dalam nested-comment, django-editorjs merupakan library editorjs untuk django digunakan dalam membuat blog , and OpenCV for picture related. Untuk selengkapnya lihat requirements.txt pada reposirory GitHub.

Link Github anggota kelompok :

https://github.com/srintikayunikharisma/django-blog.git

https://github.com/FAnisa59/django_blog

https://github.com/NolaReziyana/django-blog

https://github.com/abidasshidiqienugraha/django-blog-master

https://github.com/nikitachairunnisa
