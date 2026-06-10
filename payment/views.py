from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .services import PaymentService
from orders.models import Order

def request_payment(request):
    tx_id = request.session.get('pending_payment_tx_id')
    if not tx_id:
        messages.error(request, 'تراکنشی یافت نشد.')
        return redirect('core:home')
    
    payment_service = PaymentService()
    callback_url = request.build_absolute_uri(reverse('payment:verify'))
    
    payment_url = payment_service.start_payment(
        transaction_id=tx_id,
        description=f"پرداخت سفارش داروخانه آرمان فارما",
        callback_url=callback_url
    )
    
    if payment_url:
        return redirect(payment_url)
    else:
        messages.error(request, 'اتصال به درگاه پرداخت با خطا مواجه شد.')
        return redirect('orders:checkout')

def verify_payment(request):
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')
    
    if status == 'OK':
        from .models import Transaction
        tx = get_object_or_404(Transaction, transaction_id=authority)
        
        payment_service = PaymentService()
        success, transaction = payment_service.verify_payment(authority, tx.amount)
        
        if success:
            # Update Order
            order = Order.objects.get(id=transaction.order_id)
            order.status = 'paid'
            order.save()
            
            messages.success(request, f'پرداخت با موفقیت انجام شد. کد رهگیری: {transaction.callback_data.get("ref_id")}')
            return redirect('orders:history')
        else:
            messages.error(request, 'تایید تراکنش با خطا مواجه شد.')
    else:
        messages.error(request, 'پرداخت توسط کاربر لغو شد یا با خطا مواجه شد.')
        
    return redirect('core:home')
