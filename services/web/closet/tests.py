import factory
from django.test import TestCase
from accounts.models import User
from .models import Clothes, Outfit

# Create your tests here.


class ClothesImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Clothes

    picture = factory.django.ImageField(color="red")


class ClosetTests(TestCase):
    fixtures = ["areas", "prefectures", "parent_categories", "child_categories"]

    def setUp(self):
        user = User.objects.create(username="test1")
        c1 = Clothes.objects.create(owner=user, parent_category_id=1, category_id=1)
        c2 = Clothes.objects.create(owner=user, parent_category_id=2, category_id=7)
        c3 = Clothes.objects.create(owner=user, parent_category_id=3, category_id=11)

    def test_add_clothes(self):
        user = User.objects.get(username="test1")
        clothes = Clothes.objects.get(id=1)

        self.assertEqual(user.clothes.first(), clothes)

        self.assertFalse(clothes.picture)
        self.assertEqual(
            clothes.show_img(), f"/static/img/icon/clothes/{clothes.category.name}.jpg",
        )
        self.assertFalse(list(clothes.colors.all()))

    def test_set_outfit(self):
        user = User.objects.get(username="test1")
        c_1 = Clothes.objects.get(id=4)
        c_2 = Clothes.objects.get(id=5)
        c_3 = Clothes.objects.get(id=6)
        outfit = Outfit.objects.create(owner=user, outerwear=c_1, top=c_2, bottom=c_3)
        self.assertTrue(outfit)
