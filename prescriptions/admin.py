from django.contrib import admin
from .models import Prescription

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone_number', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['full_name', 'phone_number']
