from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _
from .models import ParentCategory, Category, Clothes

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
