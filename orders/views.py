import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from products.models import Product

def checkout(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        shipping_method = request.POST.get('shipping_method')
        payment_method = request.POST.get('payment_method')
        cart_data_raw = request.POST.get('cart_data') # Hidden field I'll add
        
        try:
            cart_data = json.loads(cart_data_raw)
        except (ValueError, TypeError):
            messages.error(request, 'خطایی در سبد خرید رخ داد.')
            return redirect('orders:checkout')

        if not cart_data:
            messages.error(request, 'سبد خرید شما خالی است.')
            return redirect('products:product_list')

        shipping_cost = 45000 if shipping_method == 'express' else 0
        
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            phone_number=phone_number,
            address=address,
            shipping_method=shipping_method,
            payment_method=payment_method,
            shipping_cost=shipping_cost
        )
        
        total_price = 0
        with transaction.atomic():
            for item in cart_data:
                product = Product.objects.select_for_update().get(id=item['id'])
                quantity = int(item['quantity'])
                
                if product.quantity < quantity:
                    messages.error(request, f'موجودی محصول {product.name} کافی نیست.')
                    return redirect('cart:detail')

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price
                )
                
                # Reduce stock
                product.quantity -= quantity
                if product.quantity == 0:
                    product.in_stock = False
                product.save()
                
                total_price += product.price * quantity
        
        order.total_price = total_price + shipping_cost
        order.save()
        
        messages.success(request, f'سفارش شماره {order.id} با موفقیت ثبت شد.')
        
        if payment_method == 'gateway':
            from payment.services import PaymentService
            payment_service = PaymentService()
            tx = payment_service.create_transaction(order.id, order.total_price)
            # Store tx id in session to retrieve it in payment view if needed
            request.session['pending_payment_tx_id'] = tx.id
            return redirect('payment:request')
        else:
            return redirect('core:home')
            
    return render(request, 'orders/checkout.html')

def tracking(request):
    order = None
    order_id = request.GET.get('order_id')
    if order_id:
        try:
            order = Order.objects.get(id=order_id)
        except (Order.DoesNotExist, ValueError):
            messages.error(request, 'سفارش مورد نظر یافت نشد. لطفا شماره سفارش را به درستی وارد کنید.')
            
    return render(request, 'orders/tracking.html', {'order': order, 'order_id': order_id})

@login_required(login_url='users:login')
def order_history(request):
    orders = request.user.orders.all()
    return render(request, 'orders/history.html', {'orders': orders})
