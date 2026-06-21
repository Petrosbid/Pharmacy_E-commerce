from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import User
import random

def login_view(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        user = authenticate(request, phone_number=phone_number, password=password)
        if user is not None:
            # Generate simulated OTP
            otp = str(random.randint(1000, 9999))
            request.session['otp_code'] = otp
            request.session['otp_phone'] = phone_number
            request.session['otp_action'] = 'login'
            request.session['pending_login_user_id'] = user.id
            
            # Print to console
            print(f"\n[OTP Simulation] SMS sent to {phone_number}: Your verification code is {otp}\n")
            messages.success(request, f"کد تایید ۴ رقمی به شماره {phone_number} پیامک شد. (کد تستی جهت شبیه‌سازی: {otp})")
            return redirect('users:verify_otp')
        else:
            messages.error(request, 'شماره موبایل یا رمز عبور اشتباه است.')
    return render(request, 'users/login.html')

def register_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        
        if User.objects.filter(phone_number=phone_number).exists():
            messages.error(request, 'این شماره موبایل قبلاً ثبت‌نام شده است.')
        else:
            # Generate simulated OTP
            otp = str(random.randint(1000, 9999))
            request.session['otp_code'] = otp
            request.session['otp_phone'] = phone_number
            request.session['otp_action'] = 'register'
            request.session['pending_register_name'] = full_name
            request.session['pending_register_phone'] = phone_number
            request.session['pending_register_password'] = password
            
            # Print to console
            print(f"\n[OTP Simulation] SMS sent to {phone_number}: Your verification code is {otp}\n")
            messages.success(request, f"کد تایید ۴ رقمی به شماره {phone_number} پیامک شد. (کد تستی جهت شبیه‌سازی: {otp})")
            return redirect('users:verify_otp')
            
    return render(request, 'users/login.html')

def verify_otp_view(request):
    otp_code = request.session.get('otp_code')
    phone_number = request.session.get('otp_phone')
    action = request.session.get('otp_action')
    
    if not otp_code or not phone_number or not action:
        messages.error(request, 'جلسه کاری شما منقضی شده است. لطفا دوباره تلاش کنید.')
        return redirect('users:login')
        
    if request.method == 'POST':
        user_otp = request.POST.get('otp_code')
        if user_otp == otp_code:
            if action == 'login':
                user_id = request.session.get('pending_login_user_id')
                try:
                    user = User.objects.get(id=user_id)
                    login(request, user)
                    messages.success(request, f'خوش آمدید، {user.full_name or user.phone_number}!')
                    _clear_otp_session(request)
                    return redirect('core:home')
                except User.DoesNotExist:
                    messages.error(request, 'کاربر مورد نظر یافت نشد.')
                    return redirect('users:login')
            elif action == 'register':
                name = request.session.get('pending_register_name')
                phone = request.session.get('pending_register_phone')
                password = request.session.get('pending_register_password')
                
                if User.objects.filter(phone_number=phone).exists():
                    messages.error(request, 'این شماره موبایل قبلاً ثبت‌نام شده است.')
                    return redirect('users:login')
                
                user = User.objects.create_user(phone_number=phone, password=password, full_name=name)
                login(request, user)
                messages.success(request, 'ثبت‌نام شما با موفقیت انجام شد.')
                _clear_otp_session(request)
                return redirect('core:home')
        else:
            messages.error(request, 'کد تایید وارد شده نادرست است.')
            
    return render(request, 'users/verify_otp.html', {'phone_number': phone_number})

def _clear_otp_session(request):
    keys_to_delete = [
        'otp_code', 'otp_phone', 'otp_action', 
        'pending_login_user_id', 'pending_register_name', 
        'pending_register_phone', 'pending_register_password'
    ]
    for key in keys_to_delete:
        request.session.pop(key, None)

def profile(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    return render(request, 'users/profile.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'شما از حساب خود خارج شدید.')
    return redirect('core:home')
