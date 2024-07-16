from django.urls import path
from django.views.generic import TemplateView
from .views import (
    BlogPostListView,
    BlogPostDetailView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView,
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    home,  # Добавьте это
)

urlpatterns = [
    # Home URL
    path('', home, name='home'),

    # BlogPost URLs
    path('blog/', BlogPostListView.as_view(), name='blog_post_list'),
    path('blog/<slug:slug>/', BlogPostDetailView.as_view(), name='blog_post_detail'),
    path('blog/new/', BlogPostCreateView.as_view(), name='blog_post_create'),
    path('blog/<int:pk>/edit/', BlogPostUpdateView.as_view(), name='blog_post_update'),
    path('blog/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blog_post_delete'),

    # Product URLs
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/new/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    # Contact URL
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),

    # About URL
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
]
