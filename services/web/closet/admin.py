from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _
from .models import (
    ParentCategory,
    Category,
    Clothes,
    Outfit,
    ClothesIndex,
    WeatherElement,
    Forecast,
    IndexCategory,
    ClothesColor,
)

# Register your models here.


class IndexCategoryInline(admin.StackedInline):
    model = IndexCategory
    extra = 0


class ClothesColorInline(admin.StackedInline):
    model = ClothesColor
    extra = 0
    ordering = ("pk",)


@admin.register(ParentCategory)
class ParentCategoryAdmin(admin.ModelAdmin):
    ordering = ("pk",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = ("pk",)
    list_display = ("name", "parent")


@admin.register(Clothes)
class ClothesAdmin(admin.ModelAdmin):
    inlines = (ClothesColorInline,)
    list_display = ("name", "owner", "parent_category", "category", "publish")
    list_filter = ("publish",)
    search_fields = ("owner",)


@admin.register(Outfit)
class OutfitAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "publish")
    list_filter = ("publish",)
    search_fields = ("owner",)


@admin.register(ClothesIndex)
class ClothesIndexAdmin(admin.ModelAdmin):
    ordering = ("pk",)
    inlines = (IndexCategoryInline,)


@admin.register(WeatherElement)
class WeatherElementAdmin(admin.ModelAdmin):
    pass


@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    list_display = ("prefecture", "created_at")
    ordering = ("-created_at",)
