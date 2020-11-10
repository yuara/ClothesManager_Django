# from django.urls import resolve
# from django.test import TestCase
# from django.http import HttpRequest
# from .views import HomePage
#
#
# class HomePageTest(TestCase):
# def test_root_url(self):
#     found = resolve("/")
#     self.assertEqual(found.func, HomePage.as_view())

# def test_home_return_title_in_html(self):
#     request = HttpRequest()
#     response = HomePage.as_view(request)
#     html = response.content.decode("utf8")
#     self.assertTrue(html.startwith("<html>"))
#     self.assertIn("<title>Home</title>", html)
#     self.assertTrue(html.endwith("<html>"))

# def test_home_return_title_in_html(self):
#     request = self.client.get('/')
#     html = response.content.decode("utf8")
#     self.assertTrue(html.startwith("<html>"))
#     self.assertIn("<title>Home</title>", html)
#     self.assertTrue(html.strip().endwith("<html>"))

# def test_home_template(self):
#     response = self.client.get("/")
#     self.assertTemplateUsed(response, "home.html")

import os
import socket
import time
import factory
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.conf import settings

# from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from closet.models import ClothesIndex


# class UserFactory(factory.django.DjangoModelFactory):
#     FACTORY_FOR = User
#
#     # username = factory.Faker("first_name")
#     # email = factory.LazyAttribute(lambda a: f"{a.username}@example.com")
#     username = "yuarakawa"
#     email = "yu.arakawa@example.com"
#     password = factory.PostGenerationMethodCall("set_password", "admin_yuarakawa")
#
#     is_superuser = True
#     is_staff = True
#     is_active = True

# os.environ["DJANGO_LIVE_TEST_SERVER_ADDRESS"] = "0.0.0.0:8000"


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
        # self.assertIn("Home", self.browser.title)
        # header_text = self.browser.find_element_by_tag_name("h1").text
        # self.assertIn("ClothesManager", header_text)
        # self.fail("Fail........")

    # def test_login(self):
    #     self.browser.get(self.live_server_url + "/accounts/login/")
    #
    #     body = self.browser.find_element_by_tag_name("body")
    #     self.assertIn("Django administration", body.text)
    #
    #     username_field = self.browser.find_element_by_name("username")
    #     username_field.send_keys(yu.username)
    #     password_field = self.browser.find_element_by_name("password")
    #     password_field.send_keys(yu.password)
    #     password_field.send_keys(Keys.RETURN)
    #
    #     self.assertIn("Dashboard - ClothesManager", self.browser.title)
    #
    # def test_admin_login(self):
    #     yu = UserFactory.create()
    #
    #     # Yu opens the browser and goes to the admin page
    #     self.browser.get(self.live_server_url + "/admin/")
    #
    #     # Yu sees the familiar 'Django Administration' heading
    #     body = self.browser.find_element_by_tag_name("body")
    #     self.assertIn("Django administration", body.text)
    #
    #     # Yu types in his username and password and hits return
    #     username_field = self.browser.find_element_by_name("username")
    #     username_field.send_keys(yu.username)
    #     password_field = self.browser.find_element_by_name("password")
    #     password_field.send_keys(yu.password)
    #     password_field.send_keys(Keys.RETURN)
    #
    #     # Yu finds himself on the 'Dashboard'
    #     body = self.browser.find_element_by_tag_name("body")
    #     self.assetrIn("Dashboard", body.text)
