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
        options.add_argument('--headless')  
        cls.driver = webdriver.Chrome(options=options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_homepage_layout(self):
        self.driver.get(self.live_server_url + '/')
        # Let the page load
        time.sleep(1)  

        # Check nav bar items
        nav_items = ['Catalog', 'Customization', 'Cart', 'Orders', 'Profile']
        for item in nav_items:
            button = self.driver.find_element(By.XPATH, f"//button[contains(text(), '{item}')]")
            self.assertIsNotNone(button)

        # Check Shop button
        shop_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Shop')]")
        self.assertIsNotNone(shop_button)

        # Check hero text
        hero_heading = self.driver.find_element(By.XPATH, "//h1[contains(text(), 'Lorem ipsum')]")
        self.assertIsNotNone(hero_heading)


class LoginPageUITests(StaticLiveServerTestCase):
    """Test suite for the login page UI of the print shop website."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        # Run browser in headless mode
        options.add_argument('--headless')  
        cls.driver = webdriver.Chrome(options=options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_login_page_ui_elements(self):
        # Update with your login URL name
        self.driver.get(self.live_server_url + reverse('login'))  

        # Check page title
        heading = self.driver.find_element(By.TAG_NAME, 'h1')
        self.assertEqual(heading.text.strip(), 'Login')

        # Check email field
        email_field = self.driver.find_element(By.CSS_SELECTOR, 'input[type="email"]')
        self.assertIsNotNone(email_field)
        self.assertEqual(email_field.get_attribute('placeholder').lower(), 'email')

        # Check password field
        password_field = self.driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
        self.assertIsNotNone(password_field)
        self.assertEqual(password_field.get_attribute('placeholder').lower(), 'password')

        # Check buttons
        sign_in_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Sign in')]")
        self.assertIsNotNone(sign_in_btn)

        create_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Create Account')]")
        self.assertIsNotNone(create_btn)

        # Check navbar buttons
        nav_items = ['Home', 'Catalog', 'Customization', 'Cart', 'Orders']
        for item in nav_items:
            btn = self.driver.find_element(By.XPATH, f"//button[contains(text(), '{item}')]")
            self.assertIsNotNone(btn)

        # Check newsletter field
        newsletter_input = self.driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter your email"]')
        self.assertIsNotNone(newsletter_input)

        subscribe_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Subscribe')]")
        self.assertIsNotNone(subscribe_button)

class SignUpPageUITests(StaticLiveServerTestCase):
    """Test suite for the sign-up page UI of the print shop website."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        # Run browser in headless mode
        options.add_argument('--headless')  
        cls.driver = webdriver.Chrome(options=options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_signup_page_ui_elements(self):
        # Update with your signup URL name
        self.driver.get(self.live_server_url + reverse('signup'))  

        # Check page title
        heading = self.driver.find_element(By.TAG_NAME, 'h1')
        self.assertEqual(heading.text.strip(), 'Create Account')

        # Check First Name field
        first_name_field = self.driver.find_element(By.CSS_SELECTOR, 'input[name="first_name"]')
        self.assertIsNotNone(first_name_field)
        self.assertEqual(first_name_field.get_attribute('placeholder').lower(), 'first name')

        # Check Last Name field
        last_name_field = self.driver.find_element(By.CSS_SELECTOR, 'input[name="last_name"]')
        self.assertIsNotNone(last_name_field)
        self.assertEqual(last_name_field.get_attribute('placeholder').lower(), 'last name')

        # Check email field
        email_field = self.driver.find_element(By.CSS_SELECTOR, 'input[type="email"]')
        self.assertIsNotNone(email_field)
        self.assertEqual(email_field.get_attribute('placeholder').lower(), 'email')

        # Check password field
        password_field = self.driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
        self.assertIsNotNone(password_field)
        self.assertEqual(password_field.get_attribute('placeholder').lower(), 'password')

        # Checkbox for Register to newsletter
        newsletter_checkbox = self.driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')
        self.assertIsNotNone(newsletter_checkbox)
        self.assertEqual(newsletter_checkbox.get_attribute('value'), 'on')

        # Check buttons
        sign_up_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Create')]")
        self.assertIsNotNone(sign_up_btn)

        login_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Sign in')]")
        self.assertIsNotNone(login_btn)

