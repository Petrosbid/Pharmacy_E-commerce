from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from products.models import Product
from .models import Cart, CartItem
import json

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        # If there was a session cart, we might want to merge it here
        # For simplicity, we just return the user cart
        return cart
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
        return cart

def cart_detail(request):
    cart = get_or_create_cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})

@require_POST
def cart_add(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({'status': 'error', 'message': 'اطلاعات نامعتبر است'}, status=400)

    product = get_object_or_404(Product, id=product_id)
    
    # Check availability
    if not product.in_stock:
        return JsonResponse({'status': 'error', 'message': 'متأسفانه این محصول در حال حاضر موجود نیست'}, status=400)

    cart = get_or_create_cart(request)
    
    with transaction.atomic():
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

    return JsonResponse({
        'status': 'success',
        'message': f'{product.name} به سبد خرید اضافه شد',
        'cart_count': cart.total_items,
        'cart_total': cart.total_price
    })

@require_POST
def cart_update(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        delta = int(data.get('delta', 0))
    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({'status': 'error', 'message': 'اطلاعات نامعتبر است'}, status=400)

    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    
    with transaction.atomic():
        cart_item.quantity += delta
        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()

    return JsonResponse({
        'status': 'success',
        'cart_count': cart.total_items,
        'cart_total': cart.total_price
    })

@require_POST
def cart_remove(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({'status': 'error', 'message': 'اطلاعات نامعتبر است'}, status=400)

    cart = get_or_create_cart(request)
    CartItem.objects.filter(cart=cart, product_id=product_id).delete()

    return JsonResponse({
        'status': 'success',
        'cart_count': cart.total_items,
        'cart_total': cart.total_price
    })

@require_POST
def cart_clear(request):
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    return JsonResponse({
        'status': 'success',
        'cart_count': 0,
        'cart_total': 0
    })

def cart_get_data(request):
    cart = get_or_create_cart(request)
    items = []
    for item in cart.items.all().select_related('product'):
        items.append({
            'id': item.product.id,
            'name': item.product.name,
            'price': item.product.price,
            'quantity': item.quantity,
            'total': item.total_price,
            'image': item.product.images.first().image.url if item.product.images.exists() else '',
            'category': item.product.category.name if item.product.category else ''
        })
    
    return JsonResponse({
        'items': items,
        'total_price': cart.total_price,
        'total_items': cart.total_items
    })
