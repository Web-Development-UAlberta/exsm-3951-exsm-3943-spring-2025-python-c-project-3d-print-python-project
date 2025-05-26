from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from store.models import (
    Orders,
    OrderItems,
    InventoryChange,
    Materials,
    Filament,
    RawMaterials,
    Suppliers,
    Shipping,
    Models,
)
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
        self.user = User.objects.create_user(username="admin", password="admin123")
        self.user.is_staff = True
        self.user.save()

        self.model = Models.objects.create(
            Name="Test Cube",
            Description="A test cube model",
            FilePath="models/cube.stl",
            Thumbnail="thumbnails/cube.jpg",
            EstimatedPrintVolume=100,
            BaseInfill=0.3,
            FixedCost=3.00,
        )

        self.material = Materials.objects.create(Name="PLA")
        self.filament = Filament.objects.create(
            Name="PLA Blue", Material=self.material, ColorHexCode="0000FF"
        )
        self.supplier = Suppliers.objects.create(
            Name="Test Supplier", Address="123 St", Phone="12345", Email="a@test.com"
        )
        self.raw_material = RawMaterials.objects.create(
            Supplier=self.supplier,
            Filament=self.filament,
            BrandName="BrandX",
            Cost=10.00,
            MaterialWeightPurchased=1000,
            MaterialDensity=1.25,
            ReorderLeadTime=5,
        )
        self.inventory = InventoryChange.objects.create(
            RawMaterial=self.raw_material, QuantityWeightAvailable=500, UnitCost=2.00
        )
        self.shipping = Shipping.objects.create(Name="Standard", Rate=5.00, ShipTime=3)
        self.order = Orders.objects.create(
            User=self.user, Shipping=self.shipping, TotalPrice=50.00
        )
        OrderItems.objects.create(
            InventoryChange=self.inventory,
            Order=self.order,
            Model=self.model,
            InfillMultiplier=1.00,
            TotalWeight=100,
            CostOfGoodsSold=10.00,
            ItemPrice=20.00,
            ItemQuantity=2,
            IsCustom=False,
        )

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
        self.browser.get(self.live_server_url + reverse("order_details", args=[self.order.id]))
        self.assertIn("Order Information", self.browser.page_source)

    ## Actions: Delete Order
    def test_order_delete_exists(self):
        self.browser.get(self.live_server_url + reverse("order_management"))
        delete_button = self.browser.find_element(By.LINK_TEXT, "Delete")
        delete_button.click()
        time.sleep(1)
        # Ensure it's redirected to confirm delete
        self.assertIn("Delete Order", self.browser.page_source)
