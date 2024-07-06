from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic.detail import DetailView
from .models import BlogPost
from .forms import BlogPostForm

class BlogPostListView(View):
    template_name = 'blog_post_list.html'

    def get(self, request):
        blog_posts = BlogPost.objects.filter(is_published=True)
        return render(request, self.template_name, {'blog_posts': blog_posts})

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_post_detail.html'
    context_object_name = 'blog_post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self):
        obj = super().get_object()
        obj.view_count += 1
        obj.save()
        return obj

class BlogPostCreateView(View):
    template_name = 'blog_post_form.html'

    def get(self, request):
        form = BlogPostForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            # Сохранение формы и генерация slug
            blog_post = form.save(commit=False)
            blog_post.slug = slugify(blog_post.title)
            blog_post.save()
            return redirect('blog_post_list')
        return render(request, self.template_name, {'form': form})

class BlogPostUpdateView(View):
    template_name = 'blog_post_form.html'

    def get(self, request, pk):
        blog_post = get_object_or_404(BlogPost, pk=pk)
        form = BlogPostForm(instance=blog_post)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        blog_post = get_object_or_404(BlogPost, pk=pk)
        form = BlogPostForm(request.POST, request.FILES, instance=blog_post)
        if form.is_valid():
            form.save()
            return redirect('blog_post_detail', slug=blog_post.slug)
        return render(request, self.template_name, {'form': form})

class BlogPostDeleteView(View):
    template_name = 'blog_post_confirm_delete.html'

    def get(self, request, pk):
        blog_post = get_object_or_404(BlogPost, pk=pk)
        return render(request, self.template_name, {'blog_post': blog_post})

    def post(self, request, pk):
        blog_post = get_object_or_404(BlogPost, pk=pk)
        blog_post.delete()
        return redirect('blog_post_list')
