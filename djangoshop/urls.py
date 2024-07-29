from django.contrib import admin
from django.urls import path, include
from catalog.views import BlogPostListView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", BlogPostListView.as_view(), name="home"),
    path("catalog/", include("catalog.urls")),
    path("users/", include("users.urls")),
]
