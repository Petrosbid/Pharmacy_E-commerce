from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .services import PaymentService
from orders.models import Order
from .models import Transaction


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
    error_code = request.GET.get('Error')

    tx = get_object_or_404(Transaction, transaction_id=authority)

    if status == 'OK':
        payment_service = PaymentService()
        success, transaction = payment_service.verify_payment(authority, tx.amount)

        if success:
            order = Order.objects.get(id=transaction.order_id)
            order.status = 'paid'
            order.save()

            request.session['result_tx_id'] = tx.id
            return redirect('payment:result')
        else:
            tx.status = 'failed'
            tx.save()
            messages.error(request, 'تایید تراکنش با خطا مواجه شد.')
    else:
        tx.status = 'failed'
        
        # Mapping error codes to user-friendly messages
        error_messages = {
            'insufficient_funds': 'موجودی حساب کافی نیست. لطفاً کارت دیگری انتخاب کرده یا موجودی حساب خود را افزایش دهید.',
            'incorrect_pin': 'رمز دوم وارد شده نادرست است. لطفاً رمز کارت خود را مجدداً بررسی کنید.',
            'expired_card': 'تاریخ انقضای کارت معتبر نیست یا کارت منقضی شده است.',
            'system_timeout': 'ارتباط با بانک صادرکننده کارت برقرار نشد. چنانچه مبلغی کسر شده است، ظرف ۷۲ ساعت آینده به حساب شما بازگردانده می‌شود.',
            'invalid_cvv2': 'کد امنیتی CVV2 نامعتبر است. لطفاً کد روی کارت را به درستی وارد کنید.',
            'user_cancel': 'تراکنش توسط کاربر لغو گردید.',
            'timer_expire': 'زمان مجاز برای انجام تراکنش به پایان رسید.',
        }
        
        msg = error_messages.get(error_code, 'پرداخت توسط کاربر لغو شد یا با خطا مواجه شد.')
        tx.callback_data = {
            'success': False,
            'error': error_code,
            'message': msg
        }
        tx.save()
        messages.error(request, msg)

    request.session['result_tx_id'] = tx.id
    return redirect('payment:result')


def payment_result(request):
    tx_id = request.session.get('result_tx_id')
    if not tx_id:
        return redirect('core:home')

    # request.session.pop('result_tx_id', None)

    transaction = get_object_or_404(Transaction, id=tx_id)
    order = Order.objects.filter(id=transaction.order_id).first()

    context = {
        'transaction': transaction,
        'order': order
    }
    return render(request, 'payment/payment_result.html', context)


def simulate_payment(request):
    authority = request.GET.get('authority')
    amount = request.GET.get('amount')
    callback = request.GET.get('callback')

    if not all([authority, amount, callback]):
        return redirect('core:home')

    context = {
        'authority': authority,
        'amount': amount,
        'callback': callback,
        'site_name': 'آرمان فارما'
    }
    return render(request, 'payment/simulate_gateway.html', context)