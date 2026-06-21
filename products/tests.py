from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Category, Product, ProductImage, Review

User = get_user_model()

class ProductModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='مکمل‌ها',
            slug='supplements',
            icon='💊',
            description='مکمل‌های غذایی و دارویی'
        )
        self.product = Product.objects.create(
            category=self.category,
            name='مولتی ویتامین',
            slug='multivitamin',
            price=120000,
            quantity=10,
            in_stock=True,
            badge='new'
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'مکمل‌ها')
        self.assertEqual(str(self.category), 'مکمل‌ها')
        self.assertEqual(self.category.get_absolute_url(), reverse('products:category_detail', kwargs={'slug': 'supplements'}))

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'مولتی ویتامین')
        self.assertEqual(str(self.product), 'مولتی ویتامین')
        self.assertEqual(self.product.get_absolute_url(), reverse('products:product_detail', kwargs={'slug': 'multivitamin'}))
        self.assertTrue(self.product.in_stock)

    def test_review_creation(self):
        user = User.objects.create_user(phone_number='09123456789', password='password123')
        review = Review.objects.create(
            product=self.product,
            user=user,
            rating=5,
            comment='بسیار عالی و با کیفیت'
        )
        self.assertEqual(review.rating, 5)
        self.assertEqual(str(review), f'09123456789 - {self.product.name} (5)')


class ProductViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name='مکمل‌ها',
            slug='supplements',
            icon='💊'
        )
        self.product1 = Product.objects.create(
            category=self.category,
            name='مولتی ویتامین',
            slug='multivitamin',
            price=120000,
            quantity=10
        )
        self.product2 = Product.objects.create(
            category=self.category,
            name='ویتامین سی',
            slug='vitamin-c',
            price=80000,
            quantity=5
        )

    def test_product_list_view(self):
        response = self.client.get(reverse('products:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_list.html')
        self.assertIn(self.product1, response.context['products'])
        self.assertIn(self.product2, response.context['products'])

    def test_product_detail_view(self):
        response = self.client.get(reverse('products:product_detail', kwargs={'slug': 'multivitamin'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertEqual(response.context['product'], self.product1)
        # Check related products
        self.assertIn(self.product2, response.context['related_products'])
        self.assertNotIn(self.product1, response.context['related_products'])

    def test_category_list_view(self):
        response = self.client.get(reverse('products:category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/category_list.html')
        self.assertIn(self.category, response.context['categories'])

    def test_category_detail_view(self):
        response = self.client.get(reverse('products:category_detail', kwargs={'slug': 'supplements'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/category_detail.html')
        self.assertEqual(response.context['category'], self.category)
        self.assertIn(self.product1, response.context['products'])

    def test_search_view_with_query(self):
        response = self.client.get(reverse('products:search'), {'q': 'ویتامین'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/search.html')
        self.assertIn(self.product1, response.context['products'])
        self.assertIn(self.product2, response.context['products'])

    def test_search_view_no_query(self):
        response = self.client.get(reverse('products:search'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 0)

    def test_favorites_view(self):
        response = self.client.get(reverse('products:favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/favorites.html')
        self.assertIn(self.product1, response.context['all_products'])
