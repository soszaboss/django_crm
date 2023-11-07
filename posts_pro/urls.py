from django.urls import path
from . import views

app_name = 'posts_pro'

urlpatterns = [
    path('', views.index, name='main'),
    path('posts/<int:number>/', views.load_data, name='main-broad'),
    path('like_post/<int:id>/', views.like_post, name='like'),
    path('unlike_post/<int:id>/', views.unlike_post, name='unlike'),
]