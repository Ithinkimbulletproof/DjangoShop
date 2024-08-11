from django.urls import path
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
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
    VersionCreateView,
    VersionUpdateView,
    VersionDeleteView,
    CategoryListView,
    home,
)

urlpatterns = [
    path("", home, name="home"),
    path("blog/", BlogPostListView.as_view(), name="blog_post_list"),
    path("blog/new/", BlogPostCreateView.as_view(), name="blog_post_create"),
    path("blog/<slug:slug>/", BlogPostDetailView.as_view(), name="blog_post_detail"),
    path("blog/<int:pk>/edit/", BlogPostUpdateView.as_view(), name="blog_post_update"),
    path(
        "blog/<int:pk>/delete/", BlogPostDeleteView.as_view(), name="blog_post_delete"
    ),
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/new/", ProductCreateView.as_view(), name="product_create"),
    path(
        "products/<int:pk>/",
        cache_page(60 * 15)(ProductDetailView.as_view()),
        name="product_detail",
    ),
    path("products/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_update"),
    path(
        "products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"
    ),
    path(
        "products/<int:product_id>/versions/new/",
        VersionCreateView.as_view(),
        name="version_create",
    ),
    path(
        "products/<int:product_id>/versions/<int:pk>/edit/",
        VersionUpdateView.as_view(),
        name="version_update",
    ),
    path(
        "products/<int:product_id>/versions/<int:pk>/delete/",
        VersionDeleteView.as_view(),
        name="version_delete",
    ),
    path(
        "contact/",
        TemplateView.as_view(template_name="catalog/contact.html"),
        name="contact",
    ),
    path(
        "about/", TemplateView.as_view(template_name="catalog/about.html"), name="about"
    ),
    path("categories/", CategoryListView.as_view(), name="category_list"),
]
