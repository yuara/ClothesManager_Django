from django.test import TestCase
from accounts.models import User

# Create your tests here.
class AccountsTests(TestCase):
    fixtures = ["areas", "prefectures"]

    def setUp(self):
        User.objects.create(username="test1")
        User.objects.create(username="test2")
        User.objects.create(username="test3")

    def test_password_hashing(self):
        u = User.objects.get(username="test1")
        u.set_password("test_password")
        self.assertFalse(u.check_password("something"))
        self.assertTrue(u.check_password("test_password"))

    def test_create_profile(self):
        u = User.objects.create(username="test_profile")
        self.assertTrue(u.profile)
        self.assertTrue(u.profile.color)
        self.assertEqual(u.profile.area.pk, 1)
        self.assertEqual(u.profile.prefecture.pk, 1)

    def test_follow(self):
        t_1 = User.objects.get(username="test1")
        t_2 = User.objects.get(username="test2")
        t_3 = User.objects.get(username="test3")
        self.assertEqual(list(t_1.following.all()), [])

        t_1.follow(t_2)
        self.assertTrue(t_1.is_following(t_2))
        t_1.follow(t_3)
        self.assertTrue(t_1.is_following(t_3))
        self.assertEquals(list(t_1.following.all()), [t_2, t_3])

        t_1.unfollow(t_3)
        self.assertEquals(list(t_1.following.all()), [t_2])
