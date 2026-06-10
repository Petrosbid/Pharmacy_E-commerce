from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products
    })

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()
    return render(request, 'products/category_detail.html', {'category': category, 'products': products})

def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'products/search.html', {'products': products, 'query': query})

def favorites(request):
    all_products = Product.objects.all()
    return render(request, 'products/favorites.html', {'all_products': all_products})
