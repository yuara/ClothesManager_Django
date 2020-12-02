from django.test import TestCase

from accounts.forms import UserCreateForm, ProfileForm


class AccountsFormsTest(TestCase):
    fixtures = ["areas", "prefectures"]

    def test_user_create_form(self):
        form = UserCreateForm(
            data={
                "username": "testuser",
                "email": "test@example.com",
                "password1": "Hello_who_am_I",
                "password2": "Hello_who_am_I",
            }
        )
        self.assertTrue(form.is_valid())

    def test_user_create_form_email(self):
        form = UserCreateForm(
            data={
                "username": "testuser",
                "email": "no_atsign_in_email",
                "password1": "Hello_who_am_I",
                "password2": "Hello_who_am_I",
            }
        )
        self.assertFalse(form.is_valid())

    def test_user_create_form_password(self):
        form = UserCreateForm(
            data={
                "username": "testuser",
                "email": "test@example.com",
                "password1": "Hello_who_am_I",
                "password2": "wrong_Hello_who_am_I",
            }
        )
        self.assertFalse(form.is_valid())

    def test_profile_form(self):
        form = ProfileForm(
            data={"area": 1, "prefecture": 1, "x": 0, "y": 0, "width": 0, "height": 0}
        )
        self.assertTrue(form.is_valid())

    def test_profile_update(self):
        form = ProfileForm(
            data={
                "area": 2,
                "prefecture": 6,
                "x": 0,
                "y": 0,
                "width": 0,
                "height": 0,
                "about_me": "Now I'm testing about me",
                "webpage": "https://www.google.com",
            }
        )
        self.assertTrue(form.is_valid())


# TODO: test uploading image
