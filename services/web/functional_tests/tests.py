import os
import socket
import time
import factory
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.conf import settings

# from django.test import LiveServerTestCase
from django.contrib.auth.hashers import make_password
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from accounts.models import User


class UserFactory(factory.django.DjangoModelFactory):
    # FACTORY_FOR = User

    # username = factory.Faker("first_name")
    # email = factory.LazyAttribute(lambda a: f"{a.username}@example.com")
    class Meta:
        model = User

    username = "yuarakawa"
    email = "yu.arakawa@example.com"
    password = factory.LazyFunction(lambda: make_password("admin_yuarakawa"))

    is_superuser = True
    is_staff = True
    is_active = True


class VisitTest(StaticLiveServerTestCase):
    live_server_url = f"http://{socket.gethostbyname(socket.gethostname())}:8000"

    def setUp(self):

        settings.DEBUG = True
        options = webdriver.ChromeOptions()
        options.binary_location = "/usr/bin/google-chrome"
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        capabilities = options.to_capabilities()

        self.browser = webdriver.Remote(
            command_executor="http://chromedriver:9515",
            desired_capabilities=capabilities,
        )

    def tesrDrop(self):
        self.browser.quit()

    def test_visit(self):
        # Access the home page of this app
        self.browser.get(self.live_server_url)

        # Confirm a title and header
        self.assertIn("Home", self.browser.title)

    # header_text = self.browser.find_element_by_tag_name("h1").text
    # self.assertIn("ClothesManager", header_text)
    # self.fail("Fail........")

    # def test_admin_login(self):
    #     yu = UserFactory()
    #     print(User.objects.all())
    #     print(yu.username)
    #     print(yu.password)
    #
    #     # Yu opens the browser and goes to the admin page
    #     self.browser.get(self.live_server_url + "/admin/")
    #
    #     # Yu types in his username and password and hits return
    #     username_field = self.browser.find_element_by_name("username")
    #     username_field.send_keys("yuarakawa")
    #     password_field = self.browser.find_element_by_name("password")
    #     password_field.send_keys("admin_yuarakawa")
    #     password_field.send_keys(Keys.RETURN)
    #
    #     # Yu sees the familiar 'Django Administration' heading
    #     body = self.browser.find_element_by_tag_name("body")
    #     self.assertIn("WELCOME", body.text)
    # print(body.text)
    # self.fail("Fail........")

    # def test_login(self):
    #     yu = UserFactory()
    #     self.browser.get(self.live_server_url + "/accounts/login/")
    #     self.assertIn("Login", self.browser.title)
    #
    #     username_field = self.browser.find_element_by_name("username")
    #     username_field.send_keys(yu.username)
    #     password_field = self.browser.find_element_by_name("password")
    #     password_field.send_keys(yu.password)
    #     password_field.send_keys(Keys.RETURN)
    #
    #     time.sleep(3)
    #     # body = self.browser.find_element_by_tag_name("body")
    #     # print(body.text)
    #     self.assertIn("Dashboard", self.browser.title)

    # TODO: not work well
    def test_signup(self):
        self.browser.get(self.live_server_url + "/accounts/signup")
        self.assertIn("Sign Up", self.browser.title)

        username_field = self.browser.find_element_by_name("username")
        username_field.send_keys("yu")
        email_field = self.browser.find_element_by_name("email")
        email_field.send_keys("yu@yu.yu")
        password_field = self.browser.find_element_by_name("password1")
        password_field.send_keys("aillenestolano")
        password2_field = self.browser.find_element_by_name("password2")
        password2_field.send_keys("aillenestolano")
        password2_field.send_keys(Keys.RETURN)

        body = self.browser.find_element_by_tag_name("body")
        self.assertIn("WELCOME", body.text)
        # self.assertIn("yu", User.objects.all())
