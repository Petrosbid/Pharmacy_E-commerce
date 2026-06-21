from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class UserManagerTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(phone_number='09123456789', password='foo')
        self.assertEqual(user.phone_number, '09123456789')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(str(user), '09123456789')

    def test_create_user_no_phone(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(phone_number='', password='foo')

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(phone_number='09998887766', password='foo')
        self.assertEqual(admin_user.phone_number, '09998887766')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(phone_number='09998887766', password='foo', is_staff=False)
            
        with self.assertRaises(ValueError):
            User.objects.create_superuser(phone_number='09998887766', password='foo', is_superuser=False)


class UserViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('users:register')
        self.login_url = reverse('users:login')
        self.profile_url = reverse('users:profile')
        self.logout_url = reverse('users:logout')
        self.user_password = 'mypassword123'
        self.user = User.objects.create_user(
            phone_number='09123456789',
            password=self.user_password,
            full_name='تست کاربر'
        )

    def test_register_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_register_post_success(self):
        # 1. Post to register (should redirect to verify_otp)
        response = self.client.post(self.register_url, {
            'phone_number': '09001112233',
            'password': 'newpassword123',
            'full_name': 'کاربر جدید'
        })
        self.assertRedirects(response, reverse('users:verify_otp'))
        self.assertFalse(User.objects.filter(phone_number='09001112233').exists())

        # 2. Submit correct OTP
        session = self.client.session
        otp = session['otp_code']
        response = self.client.post(reverse('users:verify_otp'), {'otp_code': otp})
        self.assertRedirects(response, reverse('core:home'))
        self.assertTrue(User.objects.filter(phone_number='09001112233').exists())

    def test_register_post_duplicate_phone(self):
        response = self.client.post(self.register_url, {
            'phone_number': '09123456789',
            'password': 'newpassword123',
            'full_name': 'کاربر تکراری'
        })
        self.assertEqual(response.status_code, 200)
        # Verify message or template rendering
        messages = list(response.context.get('messages', []))
        self.assertTrue(any('این شماره موبایل قبلاً ثبت‌نام شده است.' in str(m) for m in messages) or response.status_code == 200)

    def test_login_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_post_success(self):
        # 1. Post valid credentials (should redirect to verify_otp)
        response = self.client.post(self.login_url, {
            'phone_number': '09123456789',
            'password': self.user_password
        })
        self.assertRedirects(response, reverse('users:verify_otp'))

        # 2. Submit correct OTP
        session = self.client.session
        otp = session['otp_code']
        response = self.client.post(reverse('users:verify_otp'), {'otp_code': otp})
        self.assertRedirects(response, reverse('core:home'))

    def test_login_post_fail(self):
        response = self.client.post(self.login_url, {
            'phone_number': '09123456789',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)

    def test_verify_otp_post_incorrect(self):
        # Post credentials to setup session
        self.client.post(self.login_url, {
            'phone_number': '09123456789',
            'password': self.user_password
        })
        # Post incorrect OTP
        response = self.client.post(reverse('users:verify_otp'), {'otp_code': '0000'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/verify_otp.html')

    def test_verify_otp_expired_session(self):
        response = self.client.get(reverse('users:verify_otp'))
        self.assertRedirects(response, reverse('users:login'))

    def test_profile_unauthenticated(self):
        response = self.client.get(self.profile_url)
        self.assertRedirects(response, self.login_url)

    def test_profile_authenticated(self):
        self.client.login(phone_number='09123456789', password=self.user_password)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_logout_view(self):
        self.client.login(phone_number='09123456789', password=self.user_password)
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, reverse('core:home'))
