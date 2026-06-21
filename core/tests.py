from django.test import TestCase, Client
from django.urls import reverse
from products.models import Category, Product
from blog.models import BlogPost
from django.contrib.auth import get_user_model
from .models import SiteSettings, FAQ

User = get_user_model()

class CoreModelTests(TestCase):
    def test_site_settings_singleton(self):
        # 1. Load settings (should create pk=1)
        settings = SiteSettings.load()
        self.assertEqual(settings.pk, 1)
        self.assertEqual(settings.site_name, 'آرمان فارما')

        # 2. Modify and save
        settings.site_name = 'داروخانه جدید'
        settings.save()

        # 3. Load again, check it is the same record
        settings_loaded = SiteSettings.load()
        self.assertEqual(settings_loaded.pk, 1)
        self.assertEqual(settings_loaded.site_name, 'داروخانه جدید')

    def test_faq_creation(self):
        faq1 = FAQ.objects.create(question='سوال ۱؟', answer='جواب ۱', order=2)
        faq2 = FAQ.objects.create(question='سوال ۲؟', answer='جواب ۲', order=1)
        
        # Verify ordering is by 'order'
        faqs = list(FAQ.objects.all())
        self.assertEqual(faqs[0], faq2)
        self.assertEqual(faqs[1], faq1)
        self.assertEqual(str(faq1), 'سوال ۱؟')


class CoreViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='مکمل‌ها', slug='supplements')
        self.product = Product.objects.create(
            category=self.category,
            name='ویتامین دی',
            slug='vitamin-d',
            price=50000,
            quantity=5
        )
        self.user = User.objects.create_user(phone_number='09123456789', password='password123')
        self.post = BlogPost.objects.create(
            title='پست تستی',
            slug='test-post',
            author=self.user,
            excerpt='خلاصه',
            content='محتوا',
            is_published=True
        )
        self.faq = FAQ.objects.create(question='سوال تستی؟', answer='جواب تستی', order=1)

    def test_home_view(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        
        # Check context
        self.assertIn(self.product, response.context['featured_products'])
        self.assertIn(self.category, response.context['categories'])
        self.assertIn(self.post, response.context['recent_posts'])
        self.assertIn(self.faq, response.context['faqs'])
        
        # Context Processor verification
        self.assertIn('site_name', response.context)
        self.assertEqual(response.context['site_name'], 'آرمان فارما')

    def test_consultation_view(self):
        response = self.client.get(reverse('core:consultation'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'consultation.html')

    def test_faq_view(self):
        response = self.client.get(reverse('core:faq'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faq.html')
        self.assertIn(self.faq, response.context['faqs'])

    def test_returns_view(self):
        response = self.client.get(reverse('core:returns'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'returns.html')

    def test_privacy_view(self):
        response = self.client.get(reverse('core:privacy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'privacy.html')

    def test_contact_view(self):
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
