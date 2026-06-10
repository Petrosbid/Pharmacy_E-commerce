from django.http import JsonResponse
from django.shortcuts import render

def cart_detail(request):
    return render(request, 'cart/detail.html')

def cart_add(request):
    # API logic to add to cart
    return JsonResponse({'status': 'success'})

def cart_remove(request):
    # API logic to remove from cart
    return JsonResponse({'status': 'success'})
