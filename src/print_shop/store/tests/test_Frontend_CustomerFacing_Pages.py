# from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.urls import reverse
from selenium.webdriver.chrome.options import Options

import time


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
        nav_items = ["Catalog", "Customization", "Cart", "Orders", "Profile"]
        for item in nav_items:
            button = self.driver.find_element(
                By.XPATH, f"//button[contains(text(), '{item}')]"
            )
            self.assertIsNotNone(button)

        # Check Shop button
        shop_button = self.driver.find_element(
            By.XPATH, "//button[contains(text(), 'Shop')]"
        )
        self.assertIsNotNone(shop_button)

        # Check hero text
        hero_heading = self.driver.find_element(
            By.XPATH, "//h1[contains(text(), 'Lorem ipsum')]"
        )
        self.assertIsNotNone(hero_heading)


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
        heading = self.driver.find_element(By.TAG_NAME, "h1")
        self.assertEqual(heading.text.strip(), "Login")

        # Check email field
        email_field = self.driver.find_element(By.CSS_SELECTOR, 'input[type="email"]')
        self.assertIsNotNone(email_field)
        self.assertEqual(email_field.get_attribute("placeholder").lower(), "email")

        # Check password field
        password_field = self.driver.find_element(
            By.CSS_SELECTOR, 'input[type="password"]'
        )
        self.assertIsNotNone(password_field)
        self.assertEqual(
            password_field.get_attribute("placeholder").lower(), "password"
        )

        # Check buttons
        sign_in_btn = self.driver.find_element(
            By.XPATH, "//button[contains(text(), 'Sign in')]"
        )
        self.assertIsNotNone(sign_in_btn)

        create_btn = self.driver.find_element(
            By.XPATH, "//button[contains(text(), 'Create Account')]"
        )
        self.assertIsNotNone(create_btn)

        # Check navbar buttons
        nav_items = ["Home", "Catalog", "Customization", "Cart", "Orders"]
        for item in nav_items:
            btn = self.driver.find_element(
                By.XPATH, f"//button[contains(text(), '{item}')]"
            )
            self.assertIsNotNone(btn)

        # Check newsletter field
        newsletter_input = self.driver.find_element(
            By.CSS_SELECTOR, 'input[placeholder="Enter your email"]'
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

        # Check page title
        heading = self.driver.find_element(By.TAG_NAME, "h1")
        self.assertEqual(heading.text.strip(), "Create Account")

        # Check First Name field
        first_name_field = self.driver.find_element(
            By.CSS_SELECTOR, 'input[name="first_name"]'
        )
        self.assertIsNotNone(first_name_field)
        self.assertEqual(
            first_name_field.get_attribute("placeholder").lower(), "first name"
        )

        # Check Last Name field
        last_name_field = self.driver.find_element(
            By.CSS_SELECTOR, 'input[name="last_name"]'
        )
        self.assertIsNotNone(last_name_field)
        self.assertEqual(
            last_name_field.get_attribute("placeholder").lower(), "last name"
        )

        # Check email field
        email_field = self.driver.find_element(By.CSS_SELECTOR, 'input[type="email"]')
        self.assertIsNotNone(email_field)
        self.assertEqual(email_field.get_attribute("placeholder").lower(), "email")

        # Check password field
        password_field = self.driver.find_element(
            By.CSS_SELECTOR, 'input[type="password"]'
        )
        self.assertIsNotNone(password_field)
        self.assertEqual(
            password_field.get_attribute("placeholder").lower(), "password"
        )

        # Checkbox for Register to newsletter
        newsletter_checkbox = self.driver.find_element(
            By.CSS_SELECTOR, 'input[type="checkbox"]'
        )
        self.assertIsNotNone(newsletter_checkbox)
        self.assertEqual(newsletter_checkbox.get_attribute("value"), "on")

        # Check buttons
        sign_up_btn = self.driver.find_element(
            By.XPATH, "//button[contains(text(), 'Create')]"
        )
        self.assertIsNotNone(sign_up_btn)

        login_btn = self.driver.find_element(
            By.XPATH, "//button[contains(text(), 'Sign in')]"
        )
        self.assertIsNotNone(login_btn)


class ProductCatalogUITest(StaticLiveServerTestCase):
    """Test suite for the product catalog page UI of the print shop website."""

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    # Test that the product catalog page loads and displays products
    def test_catalog_page_loads(self):
        self.browser.get(self.live_server_url + "/catalog/")

        # Check if the page title is correct
        self.assertIn("Product Catalog", self.browser.title)

        # Check if the catalog header is present
        header = self.browser.find_element(By.TAG_NAME, "h1")
        self.assertEqual(header.text, "Product Catalog")

        # Check if the catalog section is present
        catalog_section = self.browser.find_element(By.ID, "catalog-section")
        self.assertIsNotNone(catalog_section)

    # Check if the catalog section contains products
    def test_catalog_page_loads_with_products(self):
        self.browser.get(self.live_server_url + "/catalog/")

        products = self.browser.find_elements(By.CLASS_NAME, "product-card")
        self.assertTrue(len(products) >= 1)

        for product in products:
            self.assertIn("Add to Cart", product.text)
            self.assertIn("Size", product.text)
            self.assertIn("Color", product.text)
            self.assertIn("Material", product.text)


class ProfileOrdersUITest(StaticLiveServerTestCase):
    """Test suite for the profile orders page UI of the print shop website."""

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    # Test that the profile page loads and displays order history
    def test_profile_order_history(self):
        self.browser.get(self.live_server_url + "/profile/")

        self.assertIn("Welcome", self.browser.page_source)
        self.assertIn("Order History", self.browser.page_source)

        orders = self.browser.find_elements(By.CLASS_NAME, "order-card")
        self.assertTrue(len(orders) >= 1)

        statuses = [o.text for o in orders]
        self.assertTrue(
            any(
                "Processing" in s or "Shipping" in s or "Completed" in s
                for s in statuses
            )
        )


class CartCheckoutUITest(StaticLiveServerTestCase):
    """Test suite for the cart checkout page UI of the print shop website."""

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    # Test that the cart page loads and displays items
    def test_cart_checkout_page_elements(self):
        self.browser.get(self.live_server_url + "/cart/")

        self.assertIn("Your Shopping Bag", self.browser.page_source)
        self.assertIn("Order Summary", self.browser.page_source)
        self.assertIn("Checkout", self.browser.page_source)

        # Test if the quantity selector is visible
        quantity_input = self.browser.find_element(By.CLASS_NAME, "quantity")
        self.assertTrue(quantity_input.is_displayed())


class OrderTrackingUITest(StaticLiveServerTestCase):
    """Test suite for the order tracking page UI of the print shop website."""

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    # Test that the order tracking page loads and displays tracking information
    def test_order_tracking_page_elements(self):
        self.browser.get(self.live_server_url + "/track-order/")

        self.assertIn("Order History", self.browser.page_source)
        self.assertIn("Order Summary", self.browser.page_source)
        self.assertIn("Track", self.browser.page_source)
