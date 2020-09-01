from django import forms
from accounts.models import User
from .models import Clothes, Outfit, ParentCategory


class ClothesCreateForm(forms.ModelForm):
    class Meta:
        model = Clothes
        fields = ("name", "note", "parent_category", "category", "publish")


class OutfitCreateForm(forms.ModelForm):
    class Meta:
        model = Outfit
        fields = (
            "name",
            "note",
            "outerwear",
            "top",
            "extra_top",
            "bottom",
            "publish",
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(OutfitCreateForm, self).__init__(*args, **kwargs)
        outerwears = ParentCategory.objects.get(name="outerwears")
        tops = ParentCategory.objects.get(name="tops")
        bottoms = ParentCategory.objects.get(name="bottoms")
        self.fields["outerwear"].queryset = Clothes.objects.filter(
            owner=user, parent_category=outerwears
        )
        self.fields["top"].queryset = Clothes.objects.filter(
            owner=user, parent_category=tops
        )
        self.fields["extra_top"].queryset = Clothes.objects.filter(
            owner=user, parent_category=tops
        )
        self.fields["bottom"].queryset = Clothes.objects.filter(
            owner=user, parent_category=bottoms
        )
