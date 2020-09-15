from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _
from .models import (
    ParentCategory,
    Category,
    Clothes,
    Outfit,
    Area,
    Prefecture,
    ClothesIndex,
    Weather,
    Forecast,
)

# Register your models here.


@admin.register(ParentCategory)
class ParentCategoryAdmin(admin.ModelAdmin):
    ordering = ("pk",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = ("pk",)


@admin.register(Clothes)
class ClothesAdmin(admin.ModelAdmin):
    pass


@admin.register(Outfit)
class OutfitAdmin(admin.ModelAdmin):
    pass


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    ordering = ("pk",)


@admin.register(Prefecture)
class PrefectureAdmin(admin.ModelAdmin):
    ordering = ("pk",)


@admin.register(ClothesIndex)
class ClothesIndexAdmin(admin.ModelAdmin):
    ordering = ("pk",)


@admin.register(Weather)
class WeatherAdmin(admin.ModelAdmin):
    pass


@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    pass
