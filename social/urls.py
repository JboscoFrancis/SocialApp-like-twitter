from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user_login/', views.userlogin, name='userlogin'),
    path('register/', views.register, name='register'),
    path('userlogout/', views.userlogout, name='userlogout'),
    path('user_profile/<str:pk>', views.user_profile, name='user_profile'),
    path('update_profile/<str:pk>', views.update_profile, name='update_profile'),
    path('edit_post/<str:pk>', views.edit_post, name='edit_post'),
     path('post_detail/<str:pk>', views.post_detail, name='post_detail'),
    path('delete_confirm/<str:pk>', views.delete_confirm, name='delete_confirm'),
    path('delete_post/<str:pk>', views.delete_post, name='delete_post'),

    path('likepost/', views.likePost, name='likePosts'),
    path('follow_user/', views.follow_user, name='follow_user'),
]