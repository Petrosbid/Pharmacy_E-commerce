from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import User

def login_view(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        user = authenticate(request, phone_number=phone_number, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'خوش آمدید، {user.full_name or user.phone_number}!')
            return redirect('core:home')
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
            user = User.objects.create_user(phone_number=phone_number, password=password, full_name=full_name)
            login(request, user)
            messages.success(request, 'ثبت‌نام شما با موفقیت انجام شد.')
            return redirect('core:home')
    return render(request, 'users/login.html')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    return render(request, 'users/profile.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'شما از حساب خود خارج شدید.')
    return redirect('core:home')
