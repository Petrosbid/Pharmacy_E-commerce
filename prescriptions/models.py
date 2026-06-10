from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Prescription(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending Review')),
        ('reviewed', _('Reviewed')),
        ('confirmed', _('Confirmed & Ready')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prescriptions', verbose_name=_('user'), null=True, blank=True)
    
    file = models.FileField(_('prescription file'), upload_to='prescriptions/')
    full_name = models.CharField(_('full name'), max_length=255)
    phone_number = models.CharField(_('phone number'), max_length=15)
    address = models.TextField(_('address'))
    notes = models.TextField(_('notes'), blank=True)
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('prescription')
        verbose_name_plural = _('prescriptions')
        ordering = ['-created_at']

    def __str__(self):
        return f'Prescription {self.id} - {self.full_name}'
