from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import UserProfiles


class UserManagementTestCase(TestCase):
    def setUp(self):
        # Create a staff user for testing
        self.admin_user = User.objects.create_user(
            username="admin", email="admin@example.com", password="admin123"
        )
        # Make the user a staff member so they can access admin views
        self.admin_user.is_staff = True
        self.admin_user.save()

        self.profile = UserProfiles.objects.get(user=self.admin_user)
        self.profile.Address = "123 Admin St"
        self.profile.Phone = "1234567890"
        self.profile.save()
        self.client.login(username="admin", password="admin123")

    ## User List View Loads
    def test_user_list_view_loads(self):
        response = self.client.get(reverse("user-profile-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "admin@example.com")

    ## Search by Name or Email
    def test_search_user_by_name(self):
        response = self.client.get(reverse("user-profile-list"), {"search": "admin"})
        self.assertContains(response, "admin")

    def test_search_user_by_email(self):
        response = self.client.get(
            reverse("user-profile-list"), {"search": "admin@example.com"}
        )
        self.assertContains(response, "admin@example.com")

    def test_filter_by_status_active(self):
        self.admin_user.is_active = True
        self.admin_user.save()
        response = self.client.get(reverse("user-profile-list"), {"status": "active"})
        self.assertContains(response, "admin")

    def test_filter_by_status_inactive(self):
        # Create an inactive user
        inactive_user = User.objects.create_user(
            username="inactive", email="inactive@example.com", password="inactive123"
        )
        inactive_user.is_active = False
        inactive_user.save()
        response = self.client.get(reverse("user-profile-list"), {"status": "inactive"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "inactive")

    ## Test Edit / Disable Actions

    def test_user_edit_view_exists(self):
        response = self.client.get(reverse("edit-user-profile", args=[self.profile.id]))
        self.assertEqual(response.status_code, 200)

    def test_user_disable_view_redirects(self):
        # Create a regular user to disable
        regular_user = User.objects.create_user(
            username="regular", email="regular@example.com", password="regular123"
        )
        regular_profile = UserProfiles.objects.get(user=regular_user)
        regular_profile.Address = "456 Regular St"
        regular_profile.Phone = "0987654321"
        regular_profile.save()

        # Prepare data to mark user as inactive using fields from UserProfileAdminForm
        form_data = {
            "username": regular_user.username,
            "first_name": regular_user.first_name,
            "last_name": regular_user.last_name,
            "email": regular_user.email,
            "is_staff": regular_user.is_staff,
            "is_active": False,  # Setting user to inactive
            "Address": regular_profile.Address,
            "Phone": regular_profile.Phone,
        }

        response = self.client.post(
            reverse("edit-user-profile", args=[regular_profile.id]), form_data
        )
        self.assertEqual(response.status_code, 302)

        # Refresh user from database and check if they're marked inactive
        regular_user.refresh_from_db()
        self.assertFalse(regular_user.is_active)
