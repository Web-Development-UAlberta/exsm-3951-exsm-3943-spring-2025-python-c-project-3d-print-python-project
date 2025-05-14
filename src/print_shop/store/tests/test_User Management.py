from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import UserProfiles


class UserManagementTestCase(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="admin", email="admin@example.com", password="admin123"
        )
        self.profile = UserProfiles.objects.get(user=self.admin_user)
        self.profile.Address = "123 Admin St"
        self.profile.Phone = "1234567890"
        self.profile.save()
        self.client.login(username="admin", password="admin123")

    ## User List View Loads
    def test_user_list_view_loads(self):
        response = self.client.get(reverse("user_management"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "admin@example.com")

    ## Search by Name or Email
    def test_search_user_by_name(self):
        response = self.client.get(reverse("user_management"), {"search": "admin"})
        self.assertContains(response, "admin")

    def test_search_user_by_email(self):
        response = self.client.get(
            reverse("user_management"), {"search": "admin@example.com"}
        )
        self.assertContains(response, "admin@example.com")

    def test_filter_by_status_active(self):
        self.admin_user.is_active = True
        self.admin_user.save()
        response = self.client.get(reverse("user_management"), {"status": "active"})
        self.assertContains(response, "admin")

    def test_filter_by_status_inactive(self):
        self.admin_user.is_active = False
        self.admin_user.save()
        response = self.client.get(reverse("user_management"), {"status": "inactive"})
        self.assertContains(response, "admin")

    ## Test Edit / Disable Actions

    def test_user_edit_view_exists(self):
        response = self.client.get(reverse("user_edit", args=[self.admin_user.id]))
        self.assertEqual(response.status_code, 200)

    def test_user_disable_view_redirects(self):
        response = self.client.post(reverse("user_disable", args=[self.admin_user.id]))
        self.assertEqual(response.status_code, 302)
        self.admin_user.refresh_from_db()
        self.assertFalse(self.admin_user.is_active)

    def test_invite_user_view_exists(self):
        response = self.client.get(reverse("user_invite"))
        self.assertEqual(response.status_code, 200)
