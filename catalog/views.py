from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Product, BlogPost, Version
from .forms import ProductForm, BlogPostForm, VersionForm
from django.contrib import messages

# Home view
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

# Product views
class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context['products']

        for product in products:
            active_version = product.versions.filter(is_current=True).first()
            product.active_version = active_version

        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        messages.success(self.request, 'Product was successfully created.')
        return super().form_valid(form)

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        messages.success(self.request, 'Product was successfully updated.')
        return super().form_valid(form)

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Product was successfully deleted.')
        return super().delete(request, *args, **kwargs)

# Version views
class VersionCreateView(CreateView):
    model = Version
    form_class = VersionForm
    template_name = 'version_form.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        product_id = self.kwargs['product_id']
        form.instance.product = get_object_or_404(Product, id=product_id)
        response = super().form_valid(form)
        if form.instance.is_current:
            Version.objects.filter(product=form.instance.product).exclude(id=form.instance.id).update(is_current=False)
        messages.success(self.request, 'Version was successfully created.')
        return response

class VersionUpdateView(UpdateView):
    model = Version
    form_class = VersionForm
    template_name = 'version_form.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.instance.is_current:
            Version.objects.filter(product=form.instance.product).exclude(id=form.instance.id).update(is_current=False)
        messages.success(self.request, 'Version was successfully updated.')
        return response

class VersionDeleteView(DeleteView):
    model = Version
    template_name = 'version_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Version was successfully deleted.')
        return super().delete(request, *args, **kwargs)

# BlogPost views
class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'catalog/blog_post_list.html'
    context_object_name = 'blog_posts'

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_post_detail.html'

class BlogPostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog_post_form.html'
    success_url = reverse_lazy('blog_post_list')

    def form_valid(self, form):
        messages.success(self.request, 'Blog post was successfully created.')
        return super().form_valid(form)

class BlogPostUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog_post_form.html'
    success_url = reverse_lazy('blog_post_list')

    def form_valid(self, form):
        messages.success(self.request, 'Blog post was successfully updated.')
        return super().form_valid(form)

class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog_post_confirm_delete.html'
    success_url = reverse_lazy('blog_post_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Blog post was successfully deleted.')
        return super().delete(request, *args, **kwargs)
