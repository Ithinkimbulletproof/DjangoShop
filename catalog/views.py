from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def contact(request):
    return render(request, 'catalog/contact.html')

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'product_detail.html', {'product': product})
