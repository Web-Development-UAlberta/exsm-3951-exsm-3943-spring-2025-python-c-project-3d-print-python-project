from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class Login_Signup_Tests(TestCase):

    def setUp(self):
        self.user_credentials = {
            'email': 'test@example.com',
            'password': 'securepass123'
        }
        self.user = User.objects.create_user(
            username=self.user_credentials['email'],
            email=self.user_credentials['email'],
            password=self.user_credentials['password']
        )

    def tearDown(self):
        self.user.delete()

    def test_login_valid_credentials(self):
        response = self.client.post(reverse('login'), {
            'email': self.user_credentials['email'],
            'password': self.user_credentials['password']
        })
        self.assertEqual(response.status_code, 302)  

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            'email': 'wrong@example.com',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "invalid")

    def test_signup_creates_user(self):
        response = self.client.post(reverse('signup'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password': 'newpassword123',
            'newsletter': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='john@example.com').exists())

    def test_signup_missing_fields(self):
        response = self.client.post(reverse('signup'), {
            'first_name': '',
            'last_name': '',
            'email': '',
            'password': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 'This field is required.')

    def test_newsletter_checkbox(self):
        response = self.client.post(reverse('signup'), {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane@example.com',
            'password': 'pass456',
            'newsletter': False
        })
        self.assertEqual(response.status_code, 302)