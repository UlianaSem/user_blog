from django.urls import path

from blog.apps import BlogConfig
from blog import views


app_name = BlogConfig.name


urlpatterns = [
    path('add_post/', views.PostCreateAPIView.as_view(), name='add_post'),
    path('delete_post/<int:pk>/', views.PostDestroyAPIView.as_view(), name='delete_post'),
    path('follow/', views.SubscriptionCreateAPIView.as_view(), name='follow'),
    path('unfollow/<int:pk>/', views.SubscriptionDestroyAPIView.as_view(), name='unfollow'),
    path('mark_read_post/', views.PostUserCreateAPIView.as_view(), name='mark_read_post'),
    path('mark_unread_post/<int:pk>/', views.PostUserDestroyAPIView.as_view(), name='mark_unread_post'),
    path('posts/', views.PostListAPIView.as_view(), name='posts_list'),
]
