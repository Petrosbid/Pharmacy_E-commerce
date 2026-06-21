from django.contrib import admin
from .models import Category, Product, ProductImage, Review

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'brand', 'dosage_form', 'is_prescription_required', 'quantity', 'in_stock', 'badge', 'rating']
    list_filter = ['category', 'in_stock', 'badge', 'is_prescription_required', 'dosage_form']
    search_fields = ['name', 'generic_name', 'brand', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    
    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'slug', 'description', 'badge')
        }),
        ('قیمت و موجودی', {
            'fields': ('price', 'old_price', 'quantity', 'in_stock')
        }),
        ('مشخصات دارویی و فنی', {
            'fields': ('generic_name', 'brand', 'dosage_form', 'dosage_strength', 'is_prescription_required')
        }),
        ('دستورالعمل‌ها', {
            'fields': ('usage_instructions', 'warnings')
        }),
        ('امتیازات', {
            'fields': ('rating', 'review_count')
        }),
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'is_verified_purchase', 'created_at']
    list_filter = ['rating', 'is_verified_purchase']
