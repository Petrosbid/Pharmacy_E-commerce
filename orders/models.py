from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('paid', _('Paid')),
        ('processing', _('Processing')),
        ('shipping', _('Shipping')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
    ]

    SHIPPING_CHOICES = [
        ('express', _('Express (2-4 hours)')),
        ('standard', _('Standard (24 hours)')),
    ]

    PAYMENT_CHOICES = [
        ('gateway', _('Online Payment')),
        ('cod', _('Cash on Delivery')),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', verbose_name=_('user'), null=True, blank=True)
    
    # Recipient Info
    full_name = models.CharField(_('full name'), max_length=255)
    phone_number = models.CharField(_('phone number'), max_length=15)
    address = models.TextField(_('address'))
    
    # Order Info
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_method = models.CharField(_('shipping method'), max_length=20, choices=SHIPPING_CHOICES, default='standard')
    payment_method = models.CharField(_('payment method'), max_length=20, choices=PAYMENT_CHOICES, default='gateway')
    
    shipping_cost = models.PositiveIntegerField(_('shipping cost'), default=0)
    total_price = models.PositiveIntegerField(_('total price'), default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        ordering = ['-created_at']

    def __str__(self):
        return f'Order {self.id} - {self.full_name}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('order'))
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name=_('product'))
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    price = models.PositiveIntegerField(_('price')) # Snapshot of price at purchase

    class Meta:
        verbose_name = _('order item')
        verbose_name_plural = _('order items')

    def __str__(self):
        return f'{self.quantity} x {self.product.name if self.product else "Deleted Product"}'

    def get_cost(self):
        return self.price * self.quantity
