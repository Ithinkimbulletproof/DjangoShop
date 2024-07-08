from django.urls import path
from .views import (
    BlogPostListView,
    BlogPostDetailView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView,
)

urlpatterns = [
    path('', BlogPostListView.as_view(), name='blog_post_list'),
    path('<slug:slug>/', BlogPostDetailView.as_view(), name='blog_post_detail'),
    path('new/', BlogPostCreateView.as_view(), name='blog_post_create'),
    path('<int:pk>/edit/', BlogPostUpdateView.as_view(), name='blog_post_update'),
    path('<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blog_post_delete'),
]
