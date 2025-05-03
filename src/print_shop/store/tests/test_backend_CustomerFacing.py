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

class SignupPageTests(TestCase):
    """Tests for the signup page functionality"""
    
    def setUp(self):
        # Create client for testing
        self.client = Client()
    
    def test_signup_page_load(self):
        """Test Load account creation page"""
        response = self.client.get(reverse('signup'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.assertContains(response, 'Create Account')
        self.assertContains(response, 'First Name')
        self.assertContains(response, 'Last Name')
        self.assertContains(response, 'Email')
        self.assertContains(response, 'Password')
        self.assertContains(response, 'newsletter')
    
    def test_valid_account_creation(self):
        """Test Valid account creation"""
        response = self.client.post(reverse('signup'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password1': 'Complex123!',
            'password2': 'Complex123!',
            'newsletter': True
        }, follow=True)
        
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('home'))
        
        # Check that user was created
        self.assertTrue(User.objects.filter(email='john.doe@example.com').exists())
        
    def test_sign_in_button(self):
        """Test Click "Sign in" button"""
        response = self.client.get(reverse('login'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
    
    def test_empty_form_submission(self):
        """Test Empty form submission"""
        response = self.client.post(reverse('signup'), {
            'first_name': '',
            'last_name': '',
            'email': '',
            'password': '',
            
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='').exists())
        self.assertFormError(response, 'form', 'first_name', 'This field is required.')
        self.assertFormError(response, 'form', 'last_name', 'This field is required.')
        self.assertFormError(response, 'form', 'email', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')
    
    def test_empty_first_name(self):
        """Test Empty first name field"""
        response = self.client.post(reverse('signup'), {
            'first_name': '',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'Complex123!',            
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='john.doe@example.com').exists())
        self.assertFormError(response, 'form', 'first_name', 'This field is required.')
    
    def test_empty_last_name(self):
        """Test Empty last name field"""
        response = self.client.post(reverse('signup'), {
            'first_name': 'John',
            'last_name': '',
            'email': 'john.doe@example.com',
            'password': 'Complex123!',
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='john.doe@example.com').exists())
        self.assertFormError(response, 'form', 'last_name', 'This field is required.')
    
    def test_empty_email(self):
        """Test Empty email field"""
        response = self.client.post(reverse('signup'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': '',
            'password': 'Complex123!'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(first_name='John', last_name='Doe').exists())
        self.assertFormError(response, 'form', 'email', 'This field is required.')
    
    def test_empty_password(self):
        """Test Empty password field"""
        response = self.client.post(reverse('signup'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': '',
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='john.doe@example.com').exists())
        self.assertFormError(response, 'form', 'password', 'This field is required.')
    
    def test_invalid_email_format(self):
        """Test Invalid email format"""
        response = self.client.post(reverse('signup'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'invalid-email',
            'password': 'Complex123!',
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(first_name='John', last_name='Doe').exists())
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')
    
    def test_password_too_short(self):
        """Test Password too short"""
        response = self.client.post(reverse('signup'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'short',
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='john.doe@example.com').exists())
        self.assertFormError(response, 'form', 'password', 'This password is too short. It must contain at least 8 characters.')
    
    def test_password_complexity(self):
        """Test password complexity validation"""
        response = self.client.post(reverse('signup'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password',  # Common password without complexity
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='john.doe@example.com').exists())
        self.assertFormError(response, 'form', 'password', 'This password is too common.')
    
    def test_duplicate_email(self):
        """Test Duplicate email submission"""
        # Create a user with the email first
        User.objects.create_user(
            username='existing@example.com',
            email='existing@example.com',
            password='testpassword123'
        )
        
        response = self.client.post(reverse('signup'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'existing@example.com',
            'password': 'Complex123!',
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 'User with this email already exists.')
    
    