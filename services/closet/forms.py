from django import forms
from .models import Clothes, ParentCategory


class ClothesCreateForm(forms.ModelForm):
    # Define parent category.
    parent_category = forms.ModelChoiceField(
        label="Parent category", queryset=ParentCategory.objects, required=False
    )

    class Meta:
        model = Clothes
        fields = ("name", "note", "category")

    field_order = ("name", "note", "parent_category", "category")
