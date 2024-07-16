from django.contrib import admin
from .models import Category, Product, BlogPost, Version

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)

class VersionInline(admin.TabularInline):
    model = Version
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'get_active_version')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    inlines = [VersionInline]
    ordering = ('name',)

    def get_active_version(self, obj):
        active_version = obj.versions.filter(is_current=True).first()
        return active_version.version_name if active_version else 'No active version'
    get_active_version.short_description = 'Active Version'

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'created_at', 'view_count')
    list_filter = ('is_published',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)

@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('product', 'version_number', 'version_name', 'is_current')
    list_filter = ('product', 'is_current')
    search_fields = ('version_number', 'version_name')
    readonly_fields = ('product',)
    ordering = ('product', 'version_number')
