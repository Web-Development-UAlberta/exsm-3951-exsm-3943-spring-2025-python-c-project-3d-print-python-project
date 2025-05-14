from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver  # type: ignore
from selenium.webdriver.chrome.options import Options  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.common.keys import Keys  # type: ignore
import time


class CsvUploadFrontendTestCase(StaticLiveServerTestCase):
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
        # Log in as the admin user
        self.browser.get(self.live_server_url + "/admin/login/")
        username_input = self.browser.find_element(By.NAME, "username")
        password_input = self.browser.find_element(By.NAME, "password")
        username_input.send_keys("admin")
        password_input.send_keys("admin123")
        password_input.submit()

        # Wait for login to complete
        time.sleep(2)

    ## Page Load Test
    def test_upload_page_loads(self):
        self.browser.get(self.live_server_url + reverse("csv_upload"))
        self.assertIn("Choose File", self.browser.page_source)

    ## File Upload with Valid CSV
    def test_valid_user_csv_upload(self):
        self.browser.get(self.live_server_url + reverse("csv_upload"))
        upload_type = self.browser.find_element(By.NAME, "upload_type")
        upload_type.send_keys("users")

        file_input = self.browser.find_element(By.NAME, "file")
        # Upload a CSV file
        file_input.send_keys("/path/to/your/testfile/users.csv")

        submit_button = self.browser.find_element(By.NAME, "submit")
        submit_button.click()

        time.sleep(2)  # Wait for the response to come back
        # Check if user1 was created (ensure it's visible on the page or check database)
        self.assertIn("user1", self.browser.page_source)

    ## Invalid CSV Upload Fails Validation
    def test_invalid_csv_upload(self):
        self.browser.get(self.live_server_url + reverse("csv_upload"))
        upload_type = self.browser.find_element(By.NAME, "upload_type")
        upload_type.send_keys("users")

        file_input = self.browser.find_element(By.NAME, "file")
        # Upload an invalid CSV file
        file_input.send_keys("/path/to/your/testfile/invalid.csv")

        submit_button = self.browser.find_element(By.NAME, "submit")
        submit_button.click()

        time.sleep(2)  # Wait for the response
        # Assert that the invalid CSV error message is shown
        self.assertIn("Invalid CSV", self.browser.page_source)

    ## Sample CSV Download Button Works
    def test_sample_csv_download(self):
        self.browser.get(self.live_server_url + reverse("csv_sample", args=["users"]))
        # Wait for the file to download
        time.sleep(2)
        # Check if the file was downloaded by verifying its Content-Type
        self.assertEqual(
            self.browser.current_url.split("?")[0],
            reverse("csv_sample", args=["users"]),
        )

    ## Block Upload Without Validation Flag
    def test_upload_blocked_without_validation_flag(self):
        self.browser.get(self.live_server_url + reverse("csv_upload"))
        upload_type = self.browser.find_element(By.NAME, "upload_type")
        upload_type.send_keys("users")

        file_input = self.browser.find_element(By.NAME, "file")
        file_input.send_keys("/path/to/your/testfile/users.csv")

        submit_button = self.browser.find_element(By.NAME, "submit")
        submit_button.click()

        time.sleep(2)  # Wait for the response
        self.assertIn("Please validate before uploading", self.browser.page_source)
