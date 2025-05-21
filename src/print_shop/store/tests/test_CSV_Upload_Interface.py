import csv
import io
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User


class CsvUploadTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="admin123")
        self.client.login(username="admin", password="admin123")

    ## Page Load Test
    def test_upload_page_loads(self):
        response = self.client.get(reverse("csv_upload"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Choose File")

    ## File Upload with Valid CSV
    def test_valid_user_csv_upload(self):
        csv_content = "username,email,password \n user1,user1@example.com,password123"
        file = SimpleUploadedFile(
            "users.csv", csv_content.encode("utf-8"), content_type="text/csv"
        )

        response = self.client.post(
            reverse("csv_upload"),
            {
                "upload_type": "users",
                "file": file,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username="user1").exists())

    ## Invalid CSV Upload Fails Validation
    def test_invalid_csv_upload(self):
        invalid_csv = "wrong_column\nvalue"
        file = SimpleUploadedFile(
            "bad.csv", invalid_csv.encode("utf-8"), content_type="text/csv"
        )

        response = self.client.post(
            reverse("csv_upload"),
            {
                "upload_type": "users",
                "file": file,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Invalid CSV")

    ##  Sample CSV Download Button Works
    def test_sample_csv_download(self):
        response = self.client.get(reverse("csv_sample", args=["users"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")

    def test_upload_blocked_without_validation_flag(self):
        csv_content = "username,email,password \n user2,user2@example.com,password123"
        file = SimpleUploadedFile(
            "users.csv", csv_content.encode("utf-8"), content_type="text/csv"
        )

        response = self.client.post(
            reverse("csv_upload"),
            {
                "upload_type": "users",
                "file": file,
            },
        )

        self.assertContains(
            response, "Please validate before uploading", status_code=400
        )
