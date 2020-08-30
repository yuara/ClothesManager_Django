from django import forms
from .models import Clothes, ParentCategory


class ClothesCreateForm(forms.ModelForm):
    class Meta:
        model = Clothes
        fields = ("name", "note", "parent_category", "category", "publish")
