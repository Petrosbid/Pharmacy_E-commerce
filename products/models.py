from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    icon = models.CharField(_('icon (emoji)'), max_length=10, blank=True)
    description = models.TextField(_('description'), blank=True)
    
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:category_detail', kwargs={'slug': self.slug})

class Product(models.Model):
    BADGE_CHOICES = [
        ('new', _('New')),
        ('sale', _('Sale')),
        ('popular', _('Popular')),
        ('bestseller', _('Bestseller')),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name=_('category'))
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'), blank=True)
    price = models.PositiveIntegerField(_('price'))
    old_price = models.PositiveIntegerField(_('old price'), null=True, blank=True)
    quantity = models.PositiveIntegerField(_('quantity'), default=0)
    in_stock = models.BooleanField(_('in stock'), default=True)
    badge = models.CharField(_('badge'), max_length=20, choices=BADGE_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Detailed pharmacy/medicinal fields
    generic_name = models.CharField(_('generic name'), max_length=255, blank=True, null=True)
    brand = models.CharField(_('brand'), max_length=255, blank=True, null=True)
    dosage_form = models.CharField(_('dosage form'), max_length=100, blank=True, null=True)
    dosage_strength = models.CharField(_('dosage strength'), max_length=100, blank=True, null=True)
    usage_instructions = models.TextField(_('usage instructions'), blank=True, null=True)
    warnings = models.TextField(_('warnings'), blank=True, null=True)
    is_prescription_required = models.BooleanField(_('is prescription required'), default=False)
    
    # Simple rating for now, can be improved with a Review model
    rating = models.DecimalField(_('rating'), max_digits=3, decimal_places=1, default=0.0)
    review_count = models.PositiveIntegerField(_('review count'), default=0)

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.slug})

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_main = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('product image')
        verbose_name_plural = _('product images')

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name=_('product'))
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='reviews', verbose_name=_('user'))
    rating = models.PositiveSmallIntegerField(_('rating'))
    comment = models.TextField(_('comment'))
    is_verified_purchase = models.BooleanField(_('verified purchase'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('review')
        verbose_name_plural = _('reviews')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.phone_number} - {self.product.name} ({self.rating})'
