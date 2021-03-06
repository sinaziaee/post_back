from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.models import Token
from rest_framework.authtoken import views as view

# http://192.168.43.126:8000/api/login/

urlpatterns = [ # 192.168.43.126:8000
    path('home/', views.home, name='home'),  # {base_url}/api/login/
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('post/all/', views.post_all, name='all'),  # {base_url}/api/post/all/
    path('post/create/', views.post_create, name='create'),  # {}/api/post/create/
    path('post/delete/<int:id>/', views.post_delete, name='delete'),
    path('post/update/<int:id>/', views.post_update, name='update'),
    path('post/get/<int:id>/', views.post_get, name='get'),  # {base_url}/api/post/get/1/
]
