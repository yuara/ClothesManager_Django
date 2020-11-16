from django.test import TestCase
from accounts.models import User

# Create your tests here.
class AccountsTests(TestCase):
    fixtures = ["areas", "prefectures"]

    def setUp(self):
        self.u1 = User.objects.create(username="Harry")
        self.u2 = User.objects.create(username="Ron")
        self.u3 = User.objects.create(username="Hermione")

    def test_password_hashing(self):
        self.u1.set_password("test_password")
        self.assertFalse(self.u1.check_password("something"))
        self.assertTrue(self.u1.check_password("test_password"))

    def test_create_profile(self):
        u = User.objects.create(username="test_profile")
        self.assertTrue(u.profile)

        self.assertEqual(u.profile.area.pk, 1)
        self.assertEqual(u.profile.prefecture.pk, 1)

    def test_follow(self):
        self.assertEqual(list(self.u1.following.all()), [])

        self.u1.follow(self.u2)
        self.assertTrue(self.u1.is_following(self.u2))
        self.u1.follow(self.u3)
        self.assertTrue(self.u1.is_following(self.u3))
        self.assertEquals(list(self.u1.following.all()), [self.u2, self.u3])

        self.u1.unfollow(self.u3)
        self.assertEquals(list(self.u1.following.all()), [self.u2])
