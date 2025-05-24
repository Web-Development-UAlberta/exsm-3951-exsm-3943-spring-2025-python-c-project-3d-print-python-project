from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth.models import User
from store.models import UserProfiles
import time


class UserManagementFrontendTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        cls.browser = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        # Create a user for testing
        self.admin_user = User.objects.create_user(
            username="admin", email="admin@example.com", password="admin123"
        )
        self.admin_user.is_staff = True
        self.admin_user.save()

        self.profile = UserProfiles.objects.get(user=self.admin_user)
        self.profile.Address = "123 Admin St"
        self.profile.Phone = "1234567890"
        self.profile.save()

        # Login to the admin account
        self.browser.get(self.live_server_url + reverse("login"))
        username_input = self.browser.find_element(By.NAME, "username")
        password_input = self.browser.find_element(By.NAME, "password")
        username_input.send_keys("admin")
        password_input.send_keys("admin123")
        password_input.submit()

        # Wait for login to complete
        time.sleep(2)

    ## User List View Loads
    def test_user_list_view_loads(self):
        self.browser.get(self.live_server_url + reverse("user-profile-list"))
        self.assertIn("admin@example.com", self.browser.page_source)

    ## Test Edit / Disable Actions
    def test_user_edit_view_exists(self):
        self.browser.get(
            self.live_server_url + reverse("edit-user-profile", args=[self.profile.id])
        )
        self.assertIn("Edit", self.browser.page_source)
        self.assertIn("User Information", self.browser.page_source)

    def test_user_delete_view_redirects(self):
        self.browser.get(self.live_server_url + reverse("user-profile-list"))
        header = WebDriverWait(self.browser, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "user-delete-button")))
        delete_button = self.browser.find_element(By.CLASS_NAME, "user-delete-button")
        delete_button.click()
        time.sleep(1)
        self.assertIn("delete the user profile", self.browser.page_source)
