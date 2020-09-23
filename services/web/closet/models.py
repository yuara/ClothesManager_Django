from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Create your models here


class IndexCategory(models.Model):
    clothes_index = models.ForeignKey("ClothesIndex", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    needs_outers = models.BooleanField(_("needs_outers"), default=False)

    class Meta:
        verbose_name = _("index category")
        verbose_name_plural = _("index categories")


class ParentCategory(models.Model):
    name = models.CharField(_("parent category name"), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("parent category")
        verbose_name_plural = _("parent categories")


class Category(models.Model):
    name = models.CharField(_("category name"), max_length=255)
    parent = models.ForeignKey(
        "ParentCategory",
        verbose_name="parent category",
        on_delete=models.PROTECT,
        related_name="child",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")


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
    picture = models.ImageField(upload_to="clothes_pic/", blank=True)
    created_at = models.DateTimeField(_("date created"), default=timezone.now)
    publish = models.BooleanField(_("publish"), default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("clothes")
        verbose_name_plural = _("clothes")


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
        blank=True,
        null=True,
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
        null=True,
    )
    bottom = models.ForeignKey(
        Clothes, verbose_name="bottom", related_name="bottom", on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(_("date created"), default=timezone.now)
    publish = models.BooleanField(_("publish"), default=False)

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(_("area"), max_length=255)

    def __str__(self):
        return self.name


class Prefecture(models.Model):
    name = models.CharField(_("prefecture"), max_length=255)
    parent = models.ForeignKey("Area", verbose_name="area", on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class ClothesIndex(models.Model):
    value = models.PositiveIntegerField(_("value"))
    description = models.TextField(_("description"), blank=True)
    categories = models.ManyToManyField("Category", through="IndexCategory", blank=True)

    def __str__(self):
        return f"value: {self.value}"

    class Meta:
        verbose_name = _("clothes index")
        verbose_name_plural = _("clothes indexes")


class Weather(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Forecast(models.Model):
    area = models.ForeignKey(
        Area, verbose_name="area", related_name="forecast", on_delete=models.PROTECT
    )
    prefecture = models.ForeignKey(
        Prefecture,
        verbose_name="prefecture",
        related_name="forecast",
        on_delete=models.PROTECT,
    )
    clothes_index = models.ForeignKey(
        ClothesIndex,
        verbose_name="clothes index",
        related_name="forecast",
        on_delete=models.PROTECT,
    )
    weather = models.ForeignKey("Weather", on_delete=models.PROTECT)
    highest_temp = models.IntegerField(_("highest tempreture"))
    lowest_temp = models.IntegerField(_("lowest tempreture"))
    rain_chance = models.IntegerField(_("rain chance"))
    created_at = models.DateTimeField(_("date created"))

    def __str__(self):
        return f"{self.prefecture} - {self.created_at}"
