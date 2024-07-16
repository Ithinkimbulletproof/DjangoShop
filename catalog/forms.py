from django import forms
from catalog.models import BlogPost, Product, Version

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'slug', 'content', 'preview_image', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'preview_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price', 'manufactured_at']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'manufactured_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['product', 'version_number', 'version_name', 'is_current']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'version_number': forms.TextInput(attrs={'class': 'form-control'}),
            'version_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_version_number(self):
        version_number = self.cleaned_data.get('version_number')
        if not version_number.isdigit():
            raise forms.ValidationError("Version number must be numeric.")
        return version_number
