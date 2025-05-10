from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
from selenium.webdriver.common.by import By # type: ignore
import time

class InventoryManagementFrontendTestCase(StaticLiveServerTestCase):

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

    ## Inventory View Loads
    def test_inventory_view_loads(self):
        self.browser.get(self.live_server_url + reverse("inventory_management"))
        # Ensure the inventory page loads with material details (ABS Red filament)
        self.assertIn("ABS Red", self.browser.page_source)

    ## Search by Material Name
    def test_inventory_search_by_material_name(self):
        self.browser.get(self.live_server_url + reverse("inventory_management"))
        search_box = self.browser.find_element(By.NAME, "search")
        search_box.send_keys("ABS")
        search_box.submit()
        time.sleep(1)
        self.assertIn("ABS", self.browser.page_source)

    ## Filter by Material
    def test_filter_by_material(self):
        self.browser.get(self.live_server_url + reverse("inventory_management"))
        material_filter = self.browser.find_element(By.NAME, "material")
        material_filter.send_keys("ABS") 
        material_filter.submit()
        time.sleep(1)
        self.assertIn("ABS", self.browser.page_source)

    ## Filter by Minimum Quantity
    def test_filter_by_quantity_min(self):
        self.browser.get(self.live_server_url + reverse("inventory_management"))
        min_quantity_filter = self.browser.find_element(By.NAME, "min_quantity")
        min_quantity_filter.send_keys("100")
        min_quantity_filter.submit()
        time.sleep(1)
        self.assertIn("100", self.browser.page_source)

    ## Actions: Edit Inventory Item
    def test_inventory_edit_view_exists(self):
        self.browser.get(self.live_server_url + reverse("inventory_edit", args=[1]))
        self.assertIn("Edit Inventory", self.browser.page_source)

    ## Actions: Delete Inventory Item
    def test_inventory_delete_view_exists(self):
        self.browser.get(self.live_server_url + reverse("inventory_management"))
        delete_button = self.browser.find_element(By.LINK_TEXT, "Delete")
        delete_button.click()
        time.sleep(1)
        # Check for redirection or confirmation that the inventory item was deleted
        self.assertNotIn("ABS Red", self.browser.page_source)
