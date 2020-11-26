from django.test import TestCase
from django.urls import reverse
from accounts.models import User


class AccountsViewsTest(TestCase):
    fixtures = ["areas", "prefectures"]

    def setUp(self):
        u1 = User.objects.create(username="test_user_1")
        u1.set_password("testing_user_1_now")
        u2 = User.objects.create(username="test_user_2")
        u2.set_password("testing_user_2_now")
        u1.save()
        u2.save()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("accounts:signup"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("accounts:signup"))
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_view_url_of_users(self):
        response = self.client.get(reverse("accounts:all"))
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("accounts:current"))
        self.assertRedirects(response, "/accounts/login/?next=/accounts/profile/")

    def test_view_url_of_current_user_profile(self):
        login = self.client.login(username="test_user_1", password="testing_user_1_now")
        response = self.client.get(reverse("accounts:current"))
        self.assertEqual(response.status_code, 200)

    def test_view_url_of_another_user_profile(self):
        login = self.client.login(username="test_user_1", password="testing_user_1_now")
        response = self.client.get(reverse("accounts:profile", args=("test_user_2",)))
        self.assertEqual(response.status_code, 200)
