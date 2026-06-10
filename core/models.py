from django.db import models
from django.utils.translation import gettext_lazy as _

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
