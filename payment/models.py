from django.db import models
from django.utils.translation import gettext_lazy as _

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('success', _('Success')),
        ('failed', _('Failed')),
    ]

    # Reusable: We use a string reference for the order to avoid direct FK if needed, 
    # but for this project we'll link it to our order. 
    # To keep it truly isolated, we could use a GenericForeignKey.
    order_id = models.CharField(_('order ID'), max_length=100)
    amount = models.PositiveIntegerField(_('amount'))
    
    transaction_id = models.CharField(_('transaction ID'), max_length=255, unique=True, null=True, blank=True)
    gateway_name = models.CharField(_('gateway name'), max_length=50)
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Raw data for auditing/debugging
    payload = models.JSONField(_('gateway payload'), null=True, blank=True)
    callback_data = models.JSONField(_('callback data'), null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')
        ordering = ['-created_at']

    def __str__(self):
        return f'Tx {self.transaction_id or self.id} - {self.status}'
