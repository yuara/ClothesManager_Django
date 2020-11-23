# from django.urls import resolve
from django.urls import reverse
from django.test import TestCase, Client
from accounts.models import User, Profile
import factory

# from django.http import HttpRequest
# from .views import HomePage
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda x: f"user_{x}")
    email = factory.LazyAttribute(lambda a: f"{a.username}@example.com")


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)


class AdminUserFactory(factory.django.DjangoModelFactory):
    # FACTORY_FOR = User

    # username = factory.Faker("first_name")
    # email = factory.LazyAttribute(lambda a: f"{a.username}@example.com")
    class Meta:
        model = User

    username = "yuarakawa"
    email = "yu.arakawa@example.com"
    password = factory.LazyFunction(lambda: make_password("admin_yuarakawa"))
    profile = factory.RelatedFactory(
        ProfileFactory, "user", area=1, prefecture=1, color="123456"
    )

    is_superuser = True
    is_staff = True
    is_active = True


class HomePageTest(TestCase):
    fixtures = ["areas", "prefectures"]

    def setUp(self):
        u = User.objects.create(
            username="test", email="test@example.com", password="test"
        )

    # def test_root_url(self):
    #     found = resolve("/")
    #     self.assertEqual(found.func, HomePage.as_view())
    #
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
    #     response = self.client.get("/index/")
    #     self.assertTemplateUsed(response, "home.html")

    def test_login_root(self):
        self.client.login(username="test", password="test")
        response = self.client.get(reverse("index"))
        html = response.content.decode("utf8")
        print(f"html------------------------\n{html}")

        # self.assertTemplateUsed(response, "index.html")
        self.assertIn("Dashboard", html)
