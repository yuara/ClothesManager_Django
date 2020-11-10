from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from .views import HomePage


class HomePageTest(TestCase):
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

    def test_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")
