from django.db import models
from django.utils.translation import gettext_lazy as _

class SiteSettings(models.Model):
    site_name = models.CharField(_('site name'), max_length=100, default='آرمان فارما')
    site_tagline = models.CharField(_('site tagline'), max_length=255, default='سلامت، اعتماد، کیفیت')
    
    phone = models.CharField(_('phone number'), max_length=20, default='۰۲۱-۸۸۸۸۸۸۸۸')
    email = models.EmailField(_('email'), default='info@armanpharma.com')
    address = models.TextField(_('address'), default='تهران، خیابان ولیعصر، نرسیده به ونک، پلاک ۱۲۳')
    working_hours = models.CharField(_('working hours'), max_length=255, default='شنبه تا پنجشنبه: ۸ صبح تا ۱۰ شب')
    
    express_shipping_cost = models.PositiveIntegerField(_('express shipping cost'), default=45000)
    
    instagram = models.URLField(blank=True, null=True, default='https://instagram.com')
    telegram = models.URLField(blank=True, null=True, default='https://t.me')
    whatsapp = models.URLField(blank=True, null=True)
    
    theme_color = models.CharField(_('primary theme color (hex)'), max_length=7, default='#0ea5e9', help_text='مانند #0ea5e9')
    hero_product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name=_('hero product'))
    
    about_us_text = models.TextField(_('about us text'), default='آرمان فارما، داروخانه آنلاین شما با ارائه بهترین و با کیفیت‌ترین محصولات بهداشتی و دارویی، همواره در تلاش است تا تجربه‌ای امن و سریع را برای شما فراهم آورد.')
    
    class Meta:
        verbose_name = _('تنظیمات سایت')
        verbose_name_plural = _('تنظیمات سایت')

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "تنظیمات سایت"


class FAQ(models.Model):
    question = models.CharField(_('question'), max_length=255)
    answer = models.TextField(_('answer'))
    order = models.PositiveIntegerField(_('order'), default=0)

    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQs')
        ordering = ['order']

    def __str__(self):
        return self.question
