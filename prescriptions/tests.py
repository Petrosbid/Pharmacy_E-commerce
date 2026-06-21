from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Prescription

User = get_user_model()

class PrescriptionModelTests(TestCase):
    def test_prescription_creation(self):
        prescription = Prescription.objects.create(
            full_name='رضا احمدی',
            phone_number='09121112233',
            address='تهران',
            notes='این یک یادداشت است'
        )
        self.assertEqual(prescription.status, 'pending')
        self.assertEqual(str(prescription), f'Prescription {prescription.id} - رضا احمدی')


class PrescriptionViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(phone_number='09123456789', password='password123')
        # Create a simple mock file
        self.mock_file = SimpleUploadedFile(
            name='prescription.pdf',
            content=b'dummy PDF content',
            content_type='application/pdf'
        )

    def test_submit_get(self):
        response = self.client.get(reverse('prescriptions:submit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'prescriptions/submit.html')

    def test_submit_post_anonymous(self):
        response = self.client.post(reverse('prescriptions:submit'), {
            'full_name': 'رضا احمدی',
            'phone_number': '09121112233',
            'address': 'تهران',
            'notes': 'یادداشت',
            'file': self.mock_file
        })
        self.assertRedirects(response, reverse('core:home'))
        
        prescription = Prescription.objects.first()
        self.assertIsNotNone(prescription)
        self.assertIsNone(prescription.user)
        self.assertEqual(prescription.full_name, 'رضا احمدی')
        self.assertTrue(prescription.file.name.endswith('.pdf'))

    def test_submit_post_authenticated(self):
        self.client.login(phone_number='09123456789', password='password123')
        response = self.client.post(reverse('prescriptions:submit'), {
            'full_name': 'علی علوی',
            'phone_number': '09123456789',
            'address': 'اصفهان',
            'notes': '',
            'file': self.mock_file
        })
        self.assertRedirects(response, reverse('core:home'))
        
        prescription = Prescription.objects.first()
        self.assertIsNotNone(prescription)
        self.assertEqual(prescription.user, self.user)
        self.assertEqual(prescription.full_name, 'علی علوی')

    def test_tracking_anonymous(self):
        response = self.client.get(reverse('prescriptions:tracking'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['prescriptions']), 0)

    def test_tracking_authenticated(self):
        prescription = Prescription.objects.create(
            user=self.user,
            full_name='علی علوی',
            phone_number='09123456789',
            address='اصفهان',
            notes=''
        )
        self.client.login(phone_number='09123456789', password='password123')
        response = self.client.get(reverse('prescriptions:tracking'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'prescriptions/tracking.html')
        self.assertIn(prescription, response.context['prescriptions'])
