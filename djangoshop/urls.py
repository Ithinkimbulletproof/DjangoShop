from django.contrib import admin
from django.urls import path, include
from .views import BlogPostListView, BlogPostDetailView, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
    path('blog/', BlogPostListView.as_view(), name='blog_post_list'),
    path('blog/', BlogPostListView.as_view(), name='blog_post_list'),
    path('blog/<slug:slug>/', BlogPostDetailView.as_view(),
         name='blog_post_detail'),
    path('blog/new/', BlogPostCreateView.as_view(),
         name='blog_post_create'),
    path('blog/<int:pk>/edit/', BlogPostUpdateView.as_view(),
         name='blog_post_update'),
    path('blog/<int:pk>/delete/', BlogPostDeleteView.as_view(),
         name='blog_post_delete'),
]
