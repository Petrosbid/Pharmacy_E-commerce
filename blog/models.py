from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import reverse

class BlogCategory(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    icon = models.CharField(_('icon (emoji)'), max_length=10, blank=True)

    class Meta:
        verbose_name = _('blog category')
        verbose_name_plural = _('blog categories')

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), unique=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name='posts', verbose_name=_('category'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts', verbose_name=_('author'))
    
    image = models.ImageField(_('image'), upload_to='blog/', null=True, blank=True)
    icon = models.CharField(_('icon (emoji)'), max_length=10, blank=True) # Fallback for card view
    
    excerpt = models.TextField(_('excerpt'))
    content = models.TextField(_('content'))
    
    read_time = models.PositiveIntegerField(_('read time (minutes)'), default=5)
    
    is_published = models.BooleanField(_('is published'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('blog post')
        verbose_name_plural = _('blog posts')
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
