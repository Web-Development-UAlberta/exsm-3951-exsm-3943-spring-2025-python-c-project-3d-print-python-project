# from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.urls import reverse
from selenium.webdriver.chrome.options import Options
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
from store.models import (
    Models,
    UserProfiles,
    Shipping,
    Orders,
    FulfillmentStatus,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from django.contrib.auth.models import User
from django.test import Client


class HomePageUITest(StaticLiveServerTestCase):
    """Test suite for the homepage UI of the print shop website."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        # Run in background
        options.add_argument("--headless")
        cls.driver = webdriver.Chrome(options=options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_homepage_layout(self):
        self.driver.get(self.live_server_url + "/")
        # Let the page load
        time.sleep(1)

        # Check nav bar items
        nav_items = ["Catalog", "Home", "Login", "Register"]
        for item in nav_items:
            button = self.driver.find_element(
                By.XPATH, f"//a[contains(text(), '{item}')]"
            )
            self.assertIsNotNone(button)

        # Check Shop button
        shop_button = self.driver.find_element(
            By.XPATH, "//a[contains(text(), 'Custom 3D Printing')]"
        )
        self.assertIsNotNone(shop_button)      


class LoginPageUITests(StaticLiveServerTestCase):
    """Test suite for the login page UI of the print shop website."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        # Run browser in headless mode
        options.add_argument("--headless")
        cls.driver = webdriver.Chrome(options=options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_login_page_ui_elements(self):
        # Update with your login URL name
        self.driver.get(self.live_server_url + reverse("login"))

        # Check page title
        heading = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1")))
        self.assertEqual(heading.text.strip(), "Welcome Back")

        # Check email field
        email_field = self.driver.find_element(By.CSS_SELECTOR, 'input[type="email"]')
        self.assertIsNotNone(email_field)
       

        # Check password field
        password_field = self.driver.find_element(
            By.CSS_SELECTOR, 'input[type="password"]'
        )
        self.assertIsNotNone(password_field)
        

        # Check buttons
        sign_in_btn = self.driver.find_element(
            By.XPATH, "//button[contains(text(), 'Sign In')]"
        )
        self.assertIsNotNone(sign_in_btn)

        create_btn = self.driver.find_element(
            By.XPATH, "//a[contains(text(), 'Register here')]"
        )
        self.assertIsNotNone(create_btn)

        # Check navbar buttons
        nav_items = ["Home", "Catalog", "Login", "Register"]
        for item in nav_items:
            btn = self.driver.find_element(
                By.XPATH, f"//a[contains(text(), '{item}')]"
            )
            self.assertIsNotNone(btn)

        # Check newsletter field
        newsletter_input = self.driver.find_element(
            By.CSS_SELECTOR, 'input[placeholder="Your email address"]'
        )
        self.assertIsNotNone(newsletter_input)

        subscribe_button = self.driver.find_element(
            By.XPATH, "//button[contains(text(), 'Subscribe')]"
        )
        self.assertIsNotNone(subscribe_button)


class SignUpPageUITests(StaticLiveServerTestCase):
    """Test suite for the sign-up page UI of the print shop website."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        # Run browser in headless mode
        options.add_argument("--headless")
        cls.driver = webdriver.Chrome(options=options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_signup_page_ui_elements(self):
        # Update with your signup URL name
        self.driver.get(self.live_server_url + reverse("register"))

        heading = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1")))
        self.assertEqual(heading.text.replace('\n', ' ').strip(), "Create Account")

        # Check First Name field
        first_name_field = self.driver.find_element(
            By.CSS_SELECTOR, 'input[name="first_name"]'
        )
        self.assertIsNotNone(first_name_field)
        
        # Check Last Name field
        last_name_field = self.driver.find_element(
            By.CSS_SELECTOR, 'input[name="last_name"]'
        )
        self.assertIsNotNone(last_name_field)
        

        # Check email field
        email_field = self.driver.find_element(By.CSS_SELECTOR, 'input[type="email"]')
        self.assertIsNotNone(email_field)
        
        # Check password field
        password_field = self.driver.find_element(
            By.CSS_SELECTOR, 'input[type="password"]'
        )
        self.assertIsNotNone(password_field)
       

        # Check buttons
        sign_up_btn = self.driver.find_element(
            By.XPATH, "//button[contains(text(), 'Register')]"
        )
        self.assertIsNotNone(sign_up_btn)

        login_btn = self.driver.find_element(
            By.XPATH, "//a[contains(text(), 'Login here')]"
        )
        self.assertIsNotNone(login_btn)


class ProductCatalogUITest(StaticLiveServerTestCase):
    """Test suite for the product catalog page UI of the print shop website."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        # Run browser in headless mode
        options.add_argument("--headless")
        cls.driver = webdriver.Chrome(options=options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        """Set up a test model."""
        # Create a test STL file
        stl_file = SimpleUploadedFile(
            "test_model.stl", b"file_content", content_type="application/sla"
        )

        # Create a test image file for thumbnail
        image_file = SimpleUploadedFile(
            "test_thumbnail.png",
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x00\x00\x02\x00\x01H\xaf\xa4q\x00\x00\x00\x00IEND\xaeB`\x82",
            content_type="image/png",
        )

        # Create a model with a thumbnail
        self.model_with_thumbnail = Models.objects.create(
            Name="3D Model With Thumbnail",
            FilePath=stl_file,
            Description="A test model with thumbnail",
            FixedCost=Decimal("100.00"),
            EstimatedPrintVolume=500,
            BaseInfill=0.2,
            Thumbnail=image_file,
        )
    # Test that the product catalog page loads and displays products
    def test_catalog_page_loads(self):
        self.driver.get(self.live_server_url + reverse("custom-gallery"))

        # Check if the catalog header is present
        header = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1")))
        self.assertEqual(header.text.strip(), "Custom 3D Printing")


    # Check if the catalog section contains products
    def test_catalog_page_loads_with_products(self):
        self.driver.get(self.live_server_url +  reverse("custom-gallery"))

        gallery_items = self.driver.find_elements(
                By.CSS_SELECTOR, ".aspect-square.bg-white.flex.items-center.justify-center")
        self.assertIsNotNone(gallery_items)
       
