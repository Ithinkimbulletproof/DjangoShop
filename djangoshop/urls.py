from django.contrib import admin
from django.urls import path, include
from catalog.views import BlogPostListView, BlogPostDetailView, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
    path('', BlogPostListView.as_view(), name='home')
]
