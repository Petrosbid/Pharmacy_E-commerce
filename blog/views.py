from django.shortcuts import render, get_object_or_404
from .models import BlogPost

def post_list(request):
    posts = BlogPost.objects.filter(is_published=True)
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})
