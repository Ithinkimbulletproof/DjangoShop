from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from .models import Product, BlogPost, Version
from .forms import ProductForm, BlogPostForm, VersionForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .services import get_cached_categories


# Home view
def home(request):
    products = Product.objects.all()
    return render(request, "catalog/home.html", {"products": products})


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = get_cached_categories()
        for product in context["products"]:
            active_version = product.versions.filter(is_current=True).first()
            product.active_version = active_version
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "catalog/product_detail.html"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("product_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Product was successfully created.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error creating the product. Please check the form for errors.",
        )
        return super().form_invalid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("product_list")

    def form_valid(self, form):
        messages.success(self.request, "Product was successfully updated.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error updating the product. Please check the form for errors.",
        )
        return super().form_invalid(form)

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        return (
            user == product.owner or
            user.has_perm('catalog.can_change_product_description') or
            user.has_perm('catalog.can_change_product_category') or
            user.has_perm('catalog.can_unpublish_product')
        )

    def get_object(self, queryset=None):
        product = super().get_object(queryset)
        user = self.request.user
        if user != product.owner and not (
            user.has_perm('catalog.can_change_product_description') or
            user.has_perm('catalog.can_change_product_category') or
            user.has_perm('catalog.can_unpublish_product')
        ):
            raise PermissionDenied("You do not have permission to edit this product.")
        return product


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("product_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Product was successfully deleted.")
        return super().delete(request, *args, **kwargs)


class VersionCreateView(CreateView):
    model = Version
    form_class = VersionForm
    template_name = "catalog/version_form.html"
    success_url = reverse_lazy("product_list")

    def form_valid(self, form):
        product_id = self.kwargs["product_id"]
        form.instance.product = get_object_or_404(Product, id=product_id)
        response = super().form_valid(form)
        if form.instance.is_current:
            Version.objects.filter(product=form.instance.product).exclude(
                id=form.instance.id
            ).update(is_current=False)
        messages.success(self.request, "Version was successfully created.")
        return response


class VersionUpdateView(UpdateView):
    model = Version
    form_class = VersionForm
    template_name = "catalog/version_form.html"
    success_url = reverse_lazy("product_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.instance.is_current:
            Version.objects.filter(product=form.instance.product).exclude(
                id=form.instance.id
            ).update(is_current=False)
        messages.success(self.request, "Version was successfully updated.")
        return response


class VersionDeleteView(DeleteView):
    model = Version
    template_name = "catalog/version_confirm_delete.html"
    success_url = reverse_lazy("product_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Version was successfully deleted.")
        return super().delete(request, *args, **kwargs)


# BlogPost views
class BlogPostListView(ListView):
    model = BlogPost
    template_name = "catalog/blog_post_list.html"
    context_object_name = "blog_posts"


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "catalog/blog_post_detail.html"
    context_object_name = "post"


class BlogPostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "catalog/blog_post_form.html"
    success_url = reverse_lazy("blog_post_list")

    def form_valid(self, form):
        messages.success(self.request, "Blog post was successfully created.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error creating the blog post. Please check the form for errors.",
        )
        return super().form_invalid(form)


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "catalog/blog_post_form.html"
    success_url = reverse_lazy("blog_post_list")

    def form_valid(self, form):
        messages.success(self.request, "Blog post was successfully updated.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error updating the blog post. Please check the form for errors.",
        )
        return super().form_invalid(form)


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = "catalog/blog_post_confirm_delete.html"
    success_url = reverse_lazy("blog_post_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Blog post was successfully deleted.")
        return super().delete(request, *args, **kwargs)

class CategoryListView(ListView):
    template_name = 'catalog/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return get_cached_categories()
