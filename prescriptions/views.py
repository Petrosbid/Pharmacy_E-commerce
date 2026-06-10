from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Prescription

def submit(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        notes = request.POST.get('notes')
        file = request.FILES.get('file')
        
        prescription = Prescription.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            phone_number=phone_number,
            address=address,
            notes=notes,
            file=file
        )
        messages.success(request, 'نسخه شما با موفقیت ثبت شد. داروساز ما بزودی برای تایید با شما تماس می‌گیرد.')
        return redirect('core:home')
        
    return render(request, 'prescriptions/submit.html')

def tracking(request):
    prescriptions = []
    if request.user.is_authenticated:
        prescriptions = request.user.prescriptions.all()
    return render(request, 'prescriptions/tracking.html', {'prescriptions': prescriptions})
