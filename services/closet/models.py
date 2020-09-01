from django.db import models
from django.conf import settings
from djchoices import ChoiceItem, DjangoChoices
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Create your models here


class ParentCategory(models.Model):
    name = models.CharField(_("parent category"), max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(_("category"), max_length=255)
    parent = models.ForeignKey(
        "ParentCategory", verbose_name="parent category", on_delete=models.PROTECT
    )

    def __str__(self):
        return self.name


class Clothes(models.Model):
    name = models.CharField(_("name"), max_length=255, blank=True)
    note = models.TextField(_("note"), blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="clothes"
    )
    parent_category = models.ForeignKey(
        ParentCategory,
        verbose_name="parent category",
        related_name="parent_category",
        on_delete=models.PROTECT,
    )
    category = models.ForeignKey(
        Category,
        verbose_name="category",
        related_name="clothes",
        on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(_("date created"), default=timezone.now)
    publish = models.BooleanField(_("publish"), default=False)

    def __str__(self):
        return self.name


class Outfit(models.Model):
    name = models.CharField(_("name"), max_length=255, blank=True)
    note = models.TextField(_("note"), blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="outfits"
    )
    outerwear = models.ForeignKey(
        Clothes,
        verbose_name="outerwear",
        related_name="outerwear",
        on_delete=models.PROTECT,
    )
    top = models.ForeignKey(
        Clothes, verbose_name="top", related_name="top", on_delete=models.PROTECT,
    )
    extra_top = models.ForeignKey(
        Clothes,
        verbose_name="extra top",
        related_name="extra_top",
        on_delete=models.PROTECT,
        blank=True,
    )
    bottom = models.ForeignKey(
        Clothes, verbose_name="bottom", related_name="bottom", on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(_("date created"), default=timezone.now)
    publish = models.BooleanField(_("publish"), default=False)

    def __str__(self):
        return self.name


# class Outfit(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(30), index=True, nullable=True)
#     note = db.Column(db.String(140), nullable=True)
#     owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     outerwear_id = db.Column(db.Integer, db.ForeignKey("clothes.id"))
#     top_1_id = db.Column(db.Integer, db.ForeignKey("clothes.id"))
#     top_2_id = db.Column(db.Integer, db.ForeignKey("clothes.id"))
#     bottom_id = db.Column(db.Integer, db.ForeignKey("clothes.id"))
#
#     outerwear = db.relationship("Clothes", foreign_keys="Outfit.outerwear_id")
#     top_1 = db.relationship("Clothes", foreign_keys="Outfit.top_1_id")
#     top_2 = db.relationship("Clothes", foreign_keys="Outfit.top_2_id")
#     bottom = db.relationship("Clothes", foreign_keys="Outfit.bottom_id")
#
#     def __repr__(self):
#         return f"<Outfit {self.name}>"
#
#
# class Forecast(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     location_id = db.Column(db.Integer, index=True)
#     clothes_index_id = db.Column(db.Integer)
#     weather = db.Column(db.String(30), nullable=True)
#     highest_temp = db.Column(db.Integer, nullable=True)
#     lowest_temp = db.Column(db.Integer, nullable=True)
#     rain_chance = db.Column(db.Integer, nullable=True)
#     update_time = db.Column(db.DateTime, index=True)
#
#     def __repr__(self):
#         return f"<Forecast {self.id}:{self.update_time}>"
#
#
# class Location(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     area_id = db.Column(db.Integer)
#     pref_id = db.Column(db.Integer)
#     city_id = db.Column(db.Integer)
#     area_name = db.Column(db.String(20))
#     pref_name = db.Column(db.String(20))
#     city_name = db.Column(db.String(20))
#
#     def __repr__(self):
#         return f"<Location {self.id}:{self.pref_name}/{self.city_name}>"
#
#
# class ClothesIndex(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     value = db.Column(db.Integer)
#     description = db.Column(db.String(140))
#     categories = db.relationship(
#         "Category", secondary=category_index, backref="category_indexes", lazy="dynamic"
#     )
#
#     def __repr__(self):
#         return f"<ClothesIndex {self.id}:{self.value}>"
