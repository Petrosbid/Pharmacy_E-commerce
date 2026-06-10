from django.core.management.base import BaseCommand
from products.models import Category, Product
from core.models import FAQ
from blog.models import BlogPost, BlogCategory
from django.utils.text import slugify
from users.models import User

class Command(BaseCommand):
    help = 'Seeds initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # Admin user
        admin_user, created = User.objects.get_or_create(
            phone_number='09120000000',
            defaults={'full_name': 'مدیر سیستم', 'is_staff': True, 'is_superuser': True}
        )
        if created:
            admin_user.set_password('admin1234')
            admin_user.save()

        # Categories
        categories_data = [
            { 'name': 'داروهای عمومی', 'icon': '💊', 'slug': 'general' },
            { 'name': 'مکمل‌ها', 'icon': '🌿', 'slug': 'supplements' },
            { 'name': 'بهداشت فردی', 'icon': '🧴', 'slug': 'hygiene' },
            { 'name': 'پوست و مو', 'icon': '✨', 'slug': 'skincare' },
            { 'name': 'مراقبت مادر و کودک', 'icon': '👶', 'slug': 'mother-child' },
            { 'name': 'تجهیزات پزشکی', 'icon': '🩺', 'slug': 'medical' },
            { 'name': 'آرایشی', 'icon': '💄', 'slug': 'cosmetics' },
            { 'name': 'محصولات نسخه‌ای', 'icon': '📋', 'slug': 'prescription' },
        ]

        for cat_data in categories_data:
            Category.objects.get_or_create(slug=cat_data['slug'], defaults={'name': cat_data['name'], 'icon': cat_data['icon']})

        # Products
        products_data = [
            { 'slug': 'vitamin-d3-5000', 'name': 'ویتامین D3 ۵۰۰۰ واحد', 'category_slug': 'supplements', 'price': 285000, 'old_price': 320000, 'badge': 'sale', 'desc': 'مکمل ویتامین D3 با جذب بالا، مناسب تقویت سیستم ایمنی و سلامت استخوان.' },
            { 'slug': 'retinol-serum-30', 'name': 'سرم ضد چروک رتینول ۳۰ml', 'category_slug': 'skincare', 'price': 890000, 'badge': 'new', 'desc': 'سرم رتینول ۰.۳٪ برای کاهش چروک و یکنواخت‌سازی رنگ پوست.' },
            { 'slug': 'multivitamin-adult', 'name': 'مولتی‌ویتامین کامل بزرگسال', 'category_slug': 'supplements', 'price': 420000, 'badge': 'bestseller', 'desc': 'فرمول کامل ۲۳ ویتامین و مواد معدنی برای بزرگسالان.' },
            { 'slug': 'hair-shampoo-400', 'name': 'شامپو تقویت‌کننده مو ۴۰۰ml', 'category_slug': 'skincare', 'price': 195000, 'old_price': 240000, 'badge': 'sale', 'desc': 'شامپو تقویت‌کننده با بیوتین و کراتین برای موهای آسیب‌دیده.' },
            { 'slug': 'protein-isolate-900', 'name': 'پودر پروتئین ایزوله ۹۰۰g', 'category_slug': 'supplements', 'price': 1250000, 'badge': 'popular', 'desc': 'پروتئین وی ایزوله ۹۰٪ با طعم وانیل، مناسب ورزشکاران.' },
        ]

        for p_data in products_data:
            cat = Category.objects.get(slug=p_data['category_slug'])
            Product.objects.get_or_create(
                slug=p_data['slug'],
                defaults={
                    'name': p_data['name'],
                    'category': cat,
                    'price': p_data['price'],
                    'old_price': p_data.get('old_price'),
                    'badge': p_data['badge'],
                    'description': p_data['desc'],
                    'rating': 4.5,
                    'review_count': 10
                }
            )

        # FAQs
        faqs_data = [
            { 'q': 'آیا خرید دارو بدون نسخه از داروخانه آنلاین مجاز است؟', 'a': 'داروهای OTC (بدون نسخه) مانند مسکن‌ها، مکمل‌ها و محصولات بهداشتی بدون محدودیت قابل خرید هستند.' },
            { 'q': 'چگونه از اصالت داروها اطمینان حاصل کنم؟', 'a': 'تمام محصولات از توزیع‌کنندگان مجاز و دارای پروانه سازمان غذا و دارو تامین می‌شوند.' },
        ]

        for faq_data in faqs_data:
            FAQ.objects.get_or_create(question=faq_data['q'], defaults={'answer': faq_data['a']})

        # Blog
        blog_cats = ['مکمل‌ها', 'دارو', 'پوست']
        for cat_name in blog_cats:
            BlogCategory.objects.get_or_create(name=cat_name, slug=slugify(cat_name, allow_unicode=True))
        
        supplement_cat = BlogCategory.objects.get(name='مکمل‌ها')
        BlogPost.objects.get_or_create(
            slug='vitamin-d-guide',
            defaults={
                'title': 'راهنمای کامل انتخاب ویتامین D — چه زمانی و چقدر مصرف کنیم؟',
                'category': supplement_cat,
                'author': admin_user,
                'excerpt': 'بررسی علمی دوز مناسب، تداخلات دارویی و علائم کمبود...',
                'content': 'متن کامل مقاله در مورد ویتامین دی...',
                'read_time': 8,
                'icon': '🌿'
            }
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded data'))
