from django.test import TestCase

from accounts.forms import UserCreateForm, ProfileForm


class AccountsFormsTest(TestCase):
    fixtures = ["areas", "prefectures"]

    def Hello_who_am_I_create_form(self):
        form = UserCreateForm(
            data={
                "username": "testuser",
                "email": "test@example.com",
                "password1": "Hello_who_am_I",
                "password2": "Hello_who_am_I",
            }
        )
        self.assertTrue(form.is_valid())

    def Hello_who_am_I_create_form_email(self):
        form = UserCreateForm(
            data={
                "username": "testuser",
                "email": "no_atsign_in_email",
                "password1": "Hello_who_am_I",
                "password2": "Hello_who_am_I",
            }
        )
        self.assertFalse(form.is_valid())

    def Hello_who_am_I_create_form_password(self):
        form = UserCreateForm(
            data={
                "username": "testuser",
                "email": "test@example.com",
                "password1": "Hello_who_am_I",
                "password2": "wrong_Hello_who_am_I",
            }
        )
        self.assertFalse(form.is_valid())
