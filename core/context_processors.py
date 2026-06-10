from products.models import Category

def site_settings(request):
    return {
        'site_name': 'آرمان فارما',
        'site_tagline': 'سلامت، اعتماد، کیفیت',
        'all_categories': Category.objects.all(),
    }
