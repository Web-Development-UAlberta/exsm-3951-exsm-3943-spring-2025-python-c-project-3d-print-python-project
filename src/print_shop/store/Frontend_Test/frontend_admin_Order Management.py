from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

class OrderManagementFrontendTestCase(StaticLiveServerTestCase):

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
        # Assuming admin is already created through the Django test database setup.
        self.browser.get(self.live_server_url + "/admin/login/")
        username_input = self.browser.find_element(By.NAME, "username")
        password_input = self.browser.find_element(By.NAME, "password")
        username_input.send_keys("admin")
        password_input.send_keys("admin123")
        password_input.submit()

        # Wait for login to complete
        time.sleep(2)

    ## Order List View Loads
    def test_order_list_view(self):
        self.browser.get(self.live_server_url + reverse("order_management"))
        # Make sure the page loads with the order details
        self.assertIn("PLA", self.browser.page_source)
        self.assertIn("50.00", self.browser.page_source) 

    ## Filter by Status
    def test_filter_by_status(self):
        self.browser.get(self.live_server_url + reverse("order_management"))
        status_filter = self.browser.find_element(By.NAME, "status")
        status_filter.send_keys("Pending")
        status_filter.submit()
        time.sleep(1)
        self.assertIn("Pending", self.browser.page_source)

    ## Filter by Material
    def test_filter_by_material(self):
        self.browser.get(self.live_server_url + reverse("order_management"))
        material_filter = self.browser.find_element(By.NAME, "material")
        material_filter.send_keys("PLA")
        material_filter.submit()
        time.sleep(1)
        self.assertIn("PLA", self.browser.page_source)

    ## Filter by Priority
    def test_filter_by_priority(self):
        self.browser.get(self.live_server_url + reverse("order_management"))
        priority_filter = self.browser.find_element(By.NAME, "priority")
        priority_filter.send_keys("High")
        priority_filter.submit()
        time.sleep(1)
        self.assertIn("High", self.browser.page_source)

    ## Search by Model Name
    def test_search_model_name(self):
        self.browser.get(self.live_server_url + reverse("order_management"))
        search_box = self.browser.find_element(By.NAME, "search")
        search_box.send_keys("Cube")
        search_box.submit()
        time.sleep(1)
        self.assertIn("Cube", self.browser.page_source)

    ## Search by Order ID
    def test_search_order_id(self):
        self.browser.get(self.live_server_url + reverse("order_management"))
        search_box = self.browser.find_element(By.NAME, "search")
        search_box.send_keys("1")
        search_box.submit()
        time.sleep(1)
        self.assertIn("1", self.browser.page_source)

    ## Actions: View Order Details
    def test_order_view_exists(self):
        self.browser.get(self.live_server_url + reverse("order_detail", args=[1])) 
        self.assertIn("Order Details", self.browser.page_source)

    ## Actions: Edit Order
    def test_order_edit_exists(self):
        self.browser.get(self.live_server_url + reverse("order_edit", args=[1])) 
        self.assertIn("Edit Order", self.browser.page_source)

    ## Actions: Delete Order
    def test_order_delete_exists(self):
        self.browser.get(self.live_server_url + reverse("order_management"))
        delete_button = self.browser.find_element(By.LINK_TEXT, "Delete")
        delete_button.click()
        time.sleep(1)
        # Ensure it's redirected or the order is deleted
        self.assertNotIn("Order ID 1", self.browser.page_source)
