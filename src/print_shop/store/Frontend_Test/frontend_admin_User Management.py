from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
from selenium.webdriver.common.by import By # type: ignore
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
        # Create an admin user
        self.admin_user = User.objects.create_user(username="admin", email="admin@example.com", password="admin123")
        
        # Create a profile for the admin user
        self.profile = UserProfiles.objects.create(user=self.admin_user, Address="123 Admin St", Phone="1234567890")

        # Login to the admin account
        self.browser.get(self.live_server_url + "/admin/login/")
        username_input = self.browser.find_element(By.NAME, "username")
        password_input = self.browser.find_element(By.NAME, "password")
        username_input.send_keys("admin")
        password_input.send_keys("admin123")
        password_input.submit()

        # Wait for login to complete
        time.sleep(2)

    ## User List View Loads
    def test_user_list_view_loads(self):
        self.browser.get(self.live_server_url + reverse("user_management"))
        self.assertIn("admin@example.com", self.browser.page_source)

    ## Search by Name or Email
    def test_search_user_by_name(self):
        self.browser.get(self.live_server_url + reverse("user_management"))
        search_box = self.browser.find_element(By.NAME, "search")
        search_box.send_keys("admin")
        search_box.submit()
        self.assertIn("admin", self.browser.page_source)

    def test_search_user_by_email(self):
        self.browser.get(self.live_server_url + reverse("user_management"))
        search_box = self.browser.find_element(By.NAME, "search")
        search_box.send_keys("admin@example.com")
        search_box.submit()
        self.assertIn("admin@example.com", self.browser.page_source)

    ## Filter by Status (Active)
    def test_filter_by_status_active(self):
        self.browser.get(self.live_server_url + reverse("user_management"))
        status_filter = self.browser.find_element(By.NAME, "status")
        status_filter.send_keys("active")
        status_filter.submit()
        time.sleep(1)
        self.assertIn("admin", self.browser.page_source)

    ## Filter by Status (Inactive)
    def test_filter_by_status_inactive(self):
        self.admin_user.is_active = False
        self.admin_user.save()
        self.browser.get(self.live_server_url + reverse("user_management"))
        status_filter = self.browser.find_element(By.NAME, "status")
        status_filter.send_keys("inactive")
        status_filter.submit()
        time.sleep(1)
        self.assertIn("admin", self.browser.page_source)

    ## Test Edit / Disable Actions
    def test_user_edit_view_exists(self):
        self.browser.get(self.live_server_url + reverse("user_edit", args=[self.admin_user.id]))
        self.assertIn("Edit User", self.browser.page_source)

    def test_user_disable_view_redirects(self):
        self.browser.get(self.live_server_url + reverse("user_management"))
        disable_button = self.browser.find_element(By.LINK_TEXT, "Disable") 
        disable_button.click()
        time.sleep(1)
        self.assertNotIn("admin", self.browser.page_source)

    ## Test Invite User View
    def test_invite_user_view_exists(self):
        self.browser.get(self.live_server_url + reverse("user_invite"))
        self.assertIn("Invite User", self.browser.page_source)
