from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.models import Token
from rest_framework.authtoken import views as view


urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    # path('register/', views.RegisterView.as_view(), name='register'),
    path('post/all/', views.post_all, name='all'),
    path('post/create/', views.post_create, name='create'),
    path('post/delete/', views.post_delete, name='delete'),
    path('post/update/', views.post_update, name='update'),
    path('post/get/<int:id>', views.post_get, name='get'),
]
