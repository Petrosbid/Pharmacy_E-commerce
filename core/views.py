from django.shortcuts import render
from products.models import Product, Category
from blog.models import BlogPost
from .models import FAQ

def home(request):
    featured_products = Product.objects.all()[:8]
    categories = Category.objects.all()
    recent_posts = BlogPost.objects.filter(is_published=True)[:3]
    faqs = FAQ.objects.all()[:5]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'recent_posts': recent_posts,
        'faqs': faqs,
    }
    return render(request, 'home.html', context)

def consultation(request):
    return render(request, 'consultation.html')

def faq(request):
    faqs = FAQ.objects.all()
    return render(request, 'faq.html', {'faqs': faqs})

def returns(request):
    return render(request, 'returns.html')

def privacy(request):
    return render(request, 'privacy.html')

def contact(request):
    return render(request, 'contact.html')
