from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import BlogCategory, BlogPost

User = get_user_model()

class BlogModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(phone_number='09123456789', password='password123')
        self.category = BlogCategory.objects.create(
            name='سلامت پوست',
            slug='skin-health',
            icon='🧴'
        )
        self.post = BlogPost.objects.create(
            title='راهنمای مراقبت از پوست',
            slug='skin-care-guide',
            category=self.category,
            author=self.user,
            excerpt='این یک خلاصه است.',
            content='این متن اصلی مقاله مراقبت از پوست است.',
            read_time=5,
            is_published=True
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'سلامت پوست')
        self.assertEqual(str(self.category), 'سلامت پوست')

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'راهنمای مراقبت از پوست')
        self.assertEqual(str(self.post), 'راهنمای مراقبت از پوست')
        self.assertEqual(self.post.get_absolute_url(), reverse('blog:post_detail', kwargs={'slug': 'skin-care-guide'}))


class BlogViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(phone_number='09123456789', password='password123')
        self.category = BlogCategory.objects.create(name='سلامت', slug='health')
        
        self.published_post = BlogPost.objects.create(
            title='مقاله منتشر شده',
            slug='published-post',
            category=self.category,
            author=self.user,
            excerpt='خلاصه',
            content='محتوا',
            is_published=True
        )
        
        self.draft_post = BlogPost.objects.create(
            title='پیش‌نویس مقاله',
            slug='draft-post',
            category=self.category,
            author=self.user,
            excerpt='خلاصه پیش‌نویس',
            content='محتوای پیش‌نویس',
            is_published=False
        )

    def test_post_list_view(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')
        self.assertIn(self.published_post, response.context['posts'])
        self.assertNotIn(self.draft_post, response.context['posts'])

    def test_post_detail_view_success(self):
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': 'published-post'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertEqual(response.context['post'], self.published_post)

    def test_post_detail_view_404(self):
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': 'non-existent-slug'}))
        self.assertEqual(response.status_code, 404)
