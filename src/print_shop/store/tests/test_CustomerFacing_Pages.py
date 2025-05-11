from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Materials, Filament, Suppliers, RawMaterials, InventoryChange, Models, UserProfiles, Shipping, Orders, OrderItems, FulfillmentStatus
from django.utils import timezone
import datetime

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
        self.assertTemplateUsed(response, 'auth/login.html')
        self.assertContains(response, 'login')
    
    def test_valid_login(self):
        """Test Valid login credentials"""
        response = self.client.post(reverse('login'), {
            'username': 'test@example.com',
            'password': 'testpassword123'
        }, follow=True)
        
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('view-profile'))
    
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
        response = self.client.get(reverse('register'))
        
        self.assertEqual(response.status_code, 200)
        
        
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
        response = self.client.get(reverse('register'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Account')
        self.assertContains(response, 'First Name')
        self.assertContains(response, 'Last Name')
        self.assertContains(response, 'Email')
        self.assertContains(response, 'Password')
        self.assertContains(response, 'newsletter')
    
    def test_valid_account_creation(self):
        """Test Valid account creation"""
        response = self.client.post(reverse('register'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password1': 'Complex123!',
            'password2': 'Complex123!',
            'newsletter': True
        }, follow=True)
        
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('login'))
        
        # Check that user was created
        self.assertTrue(User.objects.filter(email='john.doe@example.com').exists())
        
    def test_sign_in_button(self):
        """Test Click "Sign in" button"""
        response = self.client.get(reverse('login'))
        
        self.assertEqual(response.status_code, 200)
    
    def test_empty_form_submission(self):
        """Test Empty form submission"""
        response = self.client.post(reverse('register'), {
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
        response = self.client.post(reverse('register'), {
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
        response = self.client.post(reverse('register'), {
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
        response = self.client.post(reverse('register'), {
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
        response = self.client.post(reverse('register'), {
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
        response = self.client.post(reverse('register'), {
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
        response = self.client.post(reverse('register'), {
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
        response = self.client.post(reverse('register'), {
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
        
        response = self.client.post(reverse('register'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'existing@example.com',
            'password': 'Complex123!',
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 'User with this email already exists.')


class HomePageTests(TestCase):
    """Tests for the home page functionality"""
    
    def setUp(self):
        # Create client for testing
        self.client = Client()
        self.home_url = reverse('home') 

        self.product = Models.objects.create(
            Name="Test Product",
            Description="Test Description",
            FixedCost=10.00,
            EstimatedPrintVolume=100,
            BaseInfill=0.2,
        )
    
    def test_home_page_load(self):
        """Test Home page loads successfully"""
        response = self.client.get(self.home_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'hero banner')

    def test_navigation_links(self):
        """Test Navigation links on the home page"""
        response = self.client.get(self.home_url)
        
        self.assertContains(response, reverse('view-profile'))
        self.assertContains(response, reverse('cart'))
        self.assertContains(response, reverse('catalog'))
        self.assertContains(response, reverse('custom-gallery'))
        self.assertContains(response, reverse('orders-list'))
        self.assertContains(response, reverse('shop'))

    def test_search_functionality(self):
        """Test Search functionality on the home page"""
        response = self.client.get(self.home_url, {'search': 'Test'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Search results for "Test"')
    

class CatalogPageTests(TestCase):
    """Tests for the catalog page functionality"""
    
    def setUp(self):
        # Create client for testing
        self.client = Client()
        self.catalog_url = reverse('catalog') 

        self.product = Models.objects.create(
            Name="Test Product",
            Description="Test Description",
            FixedCost=10.00,
            EstimatedPrintVolume=100,
            BaseInfill=0.2,
        )

        self.material = Materials.objects.create(Name="PLA")
        self.filament = Filament.objects.create(
            Name="PLA Filament",
            Material=self.material,
            ColorHexCode="FF0000"
        )
    
    def test_catalog_page_load(self):
        """Test Catalog page loads successfully"""
        response = self.client.get(self.catalog_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Catalog')

    def test_product_display(self):
        """Test Product display on the catalog page"""
        response = self.client.get(self.catalog_url)
        
        self.assertContains(response, self.product.Name)
        self.assertContains(response, self.product.Description)
        self.assertContains(response, self.product.FixedCost)
        self.assertContains(response, self.product.EstimatedPrintVolume)
        self.assertContains(response, self.product.BaseInfill)

    
    def test_customization_options(self):
        """Test Customization options on the catalog page"""
        product_details_url = reverse('product_details', args=[self.product.id])
        response = self.client.get(product_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PLA Filament')
        self.assertContains(response, 'PLA')
        self.assertContains(response, 'FF0000')
        self.assertContains(response, 'Add to Cart')
        

    def test_add_to_cart_functionality(self):
        """Test Add to Cart functionality on the catalog page"""
        add_to_cart_url = reverse('add_to_cart', args=[self.product.id])
        response = self.client.post(add_to_cart_url, {'quantity': 1})
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart'))
        self.assertContains(response, 'Product added to cart')


class CartPageTests(TestCase):
    """Tests for the cart page functionality"""
    
    def setUp(self):
        # Create client for testing
        self.client = Client()
        self.cart_url = reverse('cart')
        self.user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            password='password123'
        )
        self.client.login(username='test@example.com', password='password123')

        self.shipping = Shipping.objects.create(
            Name="Standard Shipping",
            Rate=5.00,
            ShipTime=7,
        )   
        self.order = Orders.objects.create(
            User=self.user,
            Shipping=self.shipping,
            TotalPrice=100.00,
            EstimatedShipDate=None,
            ExpeditedService=False,
        )
        self.material = Materials.objects.create(Name="PLA")
        self.supplier = Suppliers.objects.create(
            Name="Supplier A",
            Address="123 Supplier St.",
            Phone="123-456-7890",
            Email="supplier@supplier.com",
        )
        self.filament = Filament.objects.create(
            Name="PLA Filament",
            Material=self.material,
            ColorHexCode="FF0000"
        )
        self.raw_material = RawMaterials.objects.create(
            Supplier=self.supplier,
            Filament=self.filament,
            BrandName="Brand A",
            Cost=20.00,
            MaterialWeightPurchased=1000,
            MaterialDensity=1.25,
            ReorderLeadTime=7,
            WearAndTearMultiplier=1.00,
        )
        self.inventory_change = InventoryChange.objects.create(
            RawMaterial=self.raw_material,
            QuantityWeightAvailable=500,
            UnitCost=20.00,
        )
        
        self.order_item = OrderItems.objects.create(
            InventoryChange=self.inventory_change,
            Order=self.order,
            Model="Test Product",
            InfillMultiplier=1.5,
            TotalWeight=100,
            CostOfGoodsSold=30.00,
            Markup=1.5,
            ItemPrice=45.00,
            ItemQuantity=2,
            IsCustom=False,
        )

        
    def test_cart_page_load_with_items(self):
        """Test Cart page loads successfully with items"""
        response = self.client.get(self.cart_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your Cart')
        self.assertContains(response, self.order_item.Model)
        self.assertContains(response, self.order_item.ItemQuantity)
        self.assertContains(response, self.order_item.ItemPrice)
        self.assertContains(response, self.order_item.CostOfGoodsSold)

    def test_increase_item_quantity(self):
        """Test Increase item quantity in the cart"""
        response = self.client.post(reverse('update_cart_item', args=[self.order_item.id]), {
            'quantity': 3
        }, follow=True)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.cart_url)
        
        # Check that the item quantity was updated
        self.order_item.refresh_from_db()
        self.assertEqual(self.order_item.ItemQuantity, 3)

    
    def test_decrease_item_quantity(self):
        """Test Decrease item quantity in the cart"""
        response = self.client.post(reverse('remove-from-cart', args=[self.order_item.id]), {
            'quantity': 1
        }, follow=True)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.cart_url)
        
        # Check that the item quantity was updated
        self.order_item.refresh_from_db()
        self.assertEqual(self.order_item.ItemQuantity, 1)

    def test_reduce_item_quantity_less_than_one(self):
        """Test Reduce item quantity to less than one"""
        response = self.client.post(reverse('remove-from-cart', args=[self.order_item.id]), {
            'quantity': 0
        }, follow=True)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.cart_url)
        
        # Check that the item was removed from the cart
        with self.assertRaises(OrderItems.DoesNotExist):
            OrderItems.objects.get(id=self.order_item.id)
        self.assertContains(response, 'Item removed from cart')

    def test_checkout_with_max_quantity(self):
        """Test Checkout with maximum quantity"""
        self.order_item.ItemQuantity = 10
        self.order_item.save()
        checkout_url = reverse('checkout')
        response = self.client.get(checkout_url)
        self.assertIn(response.status_code, [200, 302])

    

class ProfileOrdersPageTests(TestCase):
    """Tests for the profile page functionality"""
    
    def setUp(self):
        # Create client for testing
        self.client = Client()
        self.user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            password='testpassword123'
        )
        
        # Create user profile
        self.profile = UserProfiles.objects.create(user=self.user)
        
        self.shipping = Shipping.objects.create(
            Name="Standard Shipping",
            Rate=5.00,
            ShipTime=7,
        )
        self.order = Orders.objects.create(
            User=self.user,
            Shipping=self.shipping,
            TotalPrice=100.00,
            CreatedAt="2023-10-01",
            EstimatedShipDate=None,
            ExpeditedService=False,
        )
        self.fullfillment_status = FulfillmentStatus.objects.create(
            Order=self.order,
            Status="shipped",
        )
        self.client.login(username='test@example.com', password='testpassword123')

    def test_orders_page_load_authenticated(self):
        """Test Orders page loads successfully for authenticated user"""
       
        response = self.client.get(reverse('orders-list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test@example.com') 
       

    def test_display_processing_orders(self):
        """Test Display processing orders"""
        response = self.client.get(reverse('orders-list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Processing')
       
    def test_display_shipping_orders(self):
        """Test Display shipping orders"""
        response = self.client.get(reverse('orders-list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Shipping')
    
    def test_display_completed_orders(self):
        """Test Display completed orders"""
        response = self.client.get(reverse('profile_orders'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Completed')

    def test_signout_link(self):
        """Test Signout link"""
        response = self.client.get(reverse('logout'), follow=True)
        
        self.assertRedirects(response, reverse('login'))


class OrderTrackingPageTests(TestCase):
    """Tests for the order tracking page functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.client = Client()
        self.user_profile = self.user.user_profile
        self.user_profile.Address = "123 Test Street"
        self.user_profile.Phone = "555-1234"
        self.user_profile.save()
        
        self.shipping = Shipping.objects.create(
            Name="Basic Shipping", 
            Rate=5.99, 
            ShipTime=5
        )
        
        self.material = Materials.objects.create(Name="PLA")
        
        self.filament = Filament.objects.create(
            Name="Standard PLA",
            Material=self.material,
            ColorHexCode="FF0000"  
        )
        
        self.supplier = Suppliers.objects.create(
            Name="Filament Supply Co",
            Address="456 Supply St",
            Phone="555-5678",
            Email="supply@example.com"
        )
        
        self.raw_material = RawMaterials.objects.create(
            Supplier=self.supplier,
            Filament=self.filament,
            BrandName="PrintWell",
            Cost=20.00,
            MaterialWeightPurchased=1000,
            MaterialDensity=1.24,
            ReorderLeadTime=7,
            WearAndTearMultiplier=1.05
        )
        
        self.inventory = InventoryChange.objects.create(
            RawMaterial=self.raw_material,
            QuantityWeightAvailable=950,
            UnitCost=0.02 
        )
     
        self.model = Models.objects.create(
            Name="Test Model",
            Description="A test 3D model",
            FilePath="models/test_model.stl",
            FixedCost=2.50,
            EstimatedPrintVolume=100,
            BaseInfill=0.20
        )
        
        self.order = Orders.objects.create(
            User=self.user,
            Shipping=self.shipping,
            TotalPrice=35.75,
            EstimatedShipDate=timezone.now() + datetime.timedelta(days=7),
            ExpeditedService=False
        )
        
        self.order_item = OrderItems.objects.create(
            InventoryChange=self.inventory,
            Order=self.order,
            Model=self.model,
            InfillMultiplier=1.0,
            TotalWeight=50,
            CostOfGoodsSold=3.50,
            Markup=0.15,
            ItemPrice=29.76,
            ItemQuantity=1,
            IsCustom=False
        )
        
        self.fulfillment = FulfillmentStatus.objects.create(
            Order=self.order,
            OrderStatus=FulfillmentStatus.Status.PAID
        )

    def test_order_tracking_page_authenticated(self):
        """Test that authenticated users can access the order tracking page"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('order_tracking'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Order History")

    
    def test_order_tracking_page_unauthenticated(self):
        """Test that unauthenticated users are redirected to login"""
        response = self.client.get(reverse('order_tracking'))
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(response.url.startswith('/auth/login/'))

    def test_order_history_display(self):
        """Test that order history is displayed correctly"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('order_tracking'))
        
        self.assertContains(response, "Order History")
        self.assertContains(response, "Order Date")
        self.assertContains(response, "Order Number")
        self.assertContains(response, "Total Price")
        self.assertContains(response, "Basic Shipping")
       

    def test_order_summary_display(self):
        """Test that order summary is displayed correctly"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('order_tracking'))
        
        self.assertContains(response, "Order Summary")
        self.assertContains(response, "Delivery Address")
        self.assertContains(response, "Order subtotal")
        self.assertContains(response, "Total")


            

        

        
        