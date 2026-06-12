from products.models import Category
from .models import SiteSettings

def site_settings(request):
    settings = SiteSettings.load()
    return {
        'site_name': settings.site_name,
        'site_tagline': settings.site_tagline,
        'all_categories': Category.objects.all(),
        'site_settings': settings,
    }
