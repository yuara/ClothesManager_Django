from PIL import Image
from django import forms
from django.utils import timezone
from accounts.models import User
from .models import Clothes, Outfit, ParentCategory


class ClothesCreateForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Clothes
        fields = (
            "name",
            "note",
            "publish",
            "parent_category",
            "category",
            "picture",
            "x",
            "y",
            "width",
            "height",
        )


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
