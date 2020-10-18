from PIL import Image
from django import forms
from django.forms.models import BaseInlineFormSet
from django.utils import timezone
from accounts.models import User
from .models import Clothes, Outfit, ParentCategory, Color


class ClothesCreateForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(), initial=0)
    y = forms.FloatField(widget=forms.HiddenInput(), initial=0)
    width = forms.FloatField(widget=forms.HiddenInput(), initial=0)
    height = forms.FloatField(widget=forms.HiddenInput(), initial=0)

    def __init__(self, *args, **kwargs):
        super(ClothesCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields["picture"].widget.attrs["class"] = ""
        self.fields["publish"].widget.attrs["class"] = "form-check-input"

    class Meta:
        model = Clothes
        fields = (
            "name",
            "note",
            "parent_category",
            "category",
            "picture",
            "publish",
            "x",
            "y",
            "width",
            "height",
        )
        help_texts = {
            "picture": "App extracts 3 colors from a picture you will upload."
        }


class MyBaseFormSet(BaseInlineFormSet):
    def add_fields(self, form, index):
        super(MyBaseFormSet, self).add_fields(form, index)
        form.fields[forms.formsets.ORDERING_FIELD_NAME].widget = forms.HiddenInput()


ColorFormset = forms.inlineformset_factory(
    Clothes,
    Color,
    fields=("code",),
    formset=MyBaseFormSet,
    extra=0,
    max_num=3,
    can_delete=False,
    can_order=True,
    widgets={"code": forms.HiddenInput()},
)


class OutfitCreateForm(forms.ModelForm):
    class Meta:
        model = Outfit
        fields = (
            "name",
            "outerwear",
            "top",
            "extra_top",
            "bottom",
            "publish",
            "note",
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
