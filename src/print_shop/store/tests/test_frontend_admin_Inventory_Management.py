from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import (
    Materials,
    Filament,
    Suppliers,
    RawMaterials,
    InventoryChange,
)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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
        self.user = User.objects.create_user(username="admin", password="admin123")
        self.user.is_staff = True
        self.user.save()

        self.material = Materials.objects.create(Name="ABS")
        self.filament = Filament.objects.create(
            Name="ABS Red", Material=self.material, ColorHexCode="FF0000"
        )
        self.supplier = Suppliers.objects.create(
            Name="TestSupplier",
            Address="123 Main",
            Phone="1234567890",
            Email="test@supplier.com",
        )

        self.raw_material = RawMaterials.objects.create(
            Supplier=self.supplier,
            Filament=self.filament,
            BrandName="MakerBrand",
            Cost=20.00,
            MaterialWeightPurchased=1000,
            MaterialDensity=1.25,
            ReorderLeadTime=7,
        )

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
        self.browser.get(self.live_server_url + reverse("current-inventory"))
        # Ensure the inventory page loads with material details (ABS Red filament)
        self.assertIn("ABS Red", self.browser.page_source)

    ## Actions: Edit Inventory Item
    def test_inventory_edit_view_exists(self):
        self.browser.get(
            self.live_server_url
            + reverse("edit-raw-material", args=[self.raw_material.id])
        )
        self.assertIn("Edit", self.browser.page_source)
        self.assertIn("Update Raw Material", self.browser.page_source)
