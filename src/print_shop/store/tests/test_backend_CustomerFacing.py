from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Materials, Filament, Suppliers, RawMaterials, InventoryChange, Models, UserProfiles, Shipping, Orders, OrderItems, FulfillmentStatus

class LoginPageTests(TestCase):

    """Tests for the login page functionality"""
    
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # Create client for testing
        self.client = Client()
    
    def test_login_page_load(self):
        """Test Login page loads successfully"""
        response = self.client.get(reverse('login'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertContains(response, 'Login')
    
    def test_valid_login(self):
        """Test Valid login credentials"""
        response = self.client.post(reverse('login'), {
            'username': 'test@example.com',
            'password': 'testpassword123'
        }, follow=True)
        
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('home'))
    
    def test_logo_redirect(self):
        """Test Click logo"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_newsletter_subscription(self):
        """Test Newsletter subscription with valid email"""
        response = self.client.post(reverse('newsletter_subscribe'), {
            'email': 'newsletter@example.com'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'subscription successful')
    
    def test_create_account_redirection(self):
        """Test Create account redirection"""
        response = self.client.get(reverse('signup'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        
    def test_invalid_credentials(self):
        """Test Invalid credentials"""
        response = self.client.post(reverse('login'), {
            'username': 'test@example.com',
            'password': 'wrongpassword'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertContains(response, 'Invalid email or password')
    
    def test_empty_email_field(self):
        """Test Empty email field"""
        response = self.client.post(reverse('login'), {
            'username': '',
            'password': 'testpassword123'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertFormError(response, 'form', 'username', 'This field is required.')
    
    def test_empty_password_field(self):
        """Test Empty password field"""
        response = self.client.post(reverse('login'), {
            'username': 'test@example.com',
            'password': ''
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertFormError(response, 'form', 'password', 'This field is required.')
    
    def test_empty_all_fields(self):
        """Test Empty all fields"""
        response = self.client.post(reverse('login'), {
            'username': '',
            'password': ''
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')
    
    def test_invalid_email_format(self):
        """Test Invalid email format"""
        response = self.client.post(reverse('login'), {
            'username': 'invalid-email',
            'password': 'testpassword123'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertFormError(response, 'form', 'username', 'Enter a valid email address.')
