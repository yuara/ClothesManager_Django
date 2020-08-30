from django import forms
from .models import Clothes, ParentCategory


class ClothesCreateForm(forms.ModelForm):
    class Meta:
        model = Clothes
        fields = ("name", "note", "parent_category", "category", "publish")

    # def clean_name(self):
    #     name = self.cleaned_data.get["name"]
    #     if name is None:
    #         user = self.request.user

    # def valid(self):
    #     if form.validate_on_submit() and request.form["form_name"] == "ClothesForm":
    #     if form.name.data:
    #         _name = form.name.data
    #     else:
    #         # the added clothes will be named like t-shirt 1, pants 1
    #         # if not input the name form
    #         _category = Category.query.filter_by(id=form.child_category.data).first()
    #         _count = (
    #             current_user.own_clothes.filter_by(category_id=_category.id).count() + 1
    #         )
    #         _name = f"{_category.child_name} {_count}"
    #
