from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import generic
from .forms import ClothesCreateForm, OutfitCreateForm, ColorFormset
from accounts.models import User
from .models import ParentCategory, Category, Clothes, Outfit, Color
from django.urls import reverse_lazy
from django.http import JsonResponse, QueryDict
from django.utils import timezone
from django.conf import settings

# Create your views here.


class CreateClothes(LoginRequiredMixin, generic.CreateView):
    model = Clothes
    form_class = ClothesCreateForm
    template_name = "closet/add_clothes.html"

    def form_valid(self, form):
        clothes = form.save(commit=False)
        # Add user and date created to a clothes
        user = self.request.user
        clothes.owner = user
        clothes.created_at = timezone.now()

        # Name a clothes if user doesn't
        if not clothes.name:
            category = clothes.category
            count_clothes = user.clothes.filter(category=category).count()
            clothes.name = f"{category} {count_clothes + 1}"

        clothes.save()

        # Get cropping positions
        x = float(self.request.POST.get("x"))
        y = float(self.request.POST.get("y"))
        w = float(self.request.POST.get("width"))
        h = float(self.request.POST.get("height"))

        # Crop if the cropping positions
        if x != 0 and y != 0 and w != 0 and h != 0:
            clothes.crop_picture(x, y, w, h)
            clothes.extract_color()
        else:
            # Create 3 color objects if no cropped image and colors
            if not clothes.colors.all():
                for i in range(3):
                    Color.objects.create(clothes=clothes, code="rgba(255, 255, 255, 1)")

        messages.info(
            self.request, f"Added {clothes.name} successfully.",
        )
        return redirect("closet:clothes")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["add_or_edit"] = "Add"
        return context


# def add_clothes(request):
#     form = ClothesCreateForm(
#         request.POST or None, files=request.FILES
#     )  # request.FILESが必要
#     context = {"form": form, "add_or_edit": "Add"}
#
#     if request.method == "POST" and form.is_valid():
# clothes = form.save(commit=False)
# Add user and date created in a clothes
# user = self.request.user
# clothes.owner = user
# clothes.created_at = timezone.now()
#
# if not clothes.name:
#     category = clothes.category
#     count_clothes = user.clothes.filter(category=category).count()
#     clothes.name = f"{category} {count_clothes + 1}"
#
# clothes.save()
#
#         x = float(self.request.POST.get("x"))
#         y = float(self.request.POST.get("y"))
#         w = float(self.request.POST.get("width"))
#         h = float(self.request.POST.get("height"))
#
#         clothes.crop_picture(x, y, w, h)
#         clothes.extract_color()
#
#         messages.info(
#             self.request,
#             f"{clothes.owner.username} added {clothes.name} successfully.",
#         )
#
#         formset = ColorFormset(request.POST, instance=clothes)
#         if formset.is_valid():
#             formset.save()
#             return redirect("app:index")
#
#         # エラーメッセージつきのformsetをテンプレートへ渡すため、contextに格納
#         else:
#             context["formset"] = formset
#
#         return redirect("closet:clothes")
#
#     # GETのとき
#     else:
#         # 空のformsetをテンプレートへ渡す
#         context["formset"] = ColorFormset()
#
#     return render(request, "closet/add_clothes.html", context)


def edit_clothes(request, pk):
    clothes = get_object_or_404(Clothes, pk=pk)
    form = ClothesCreateForm(
        request.POST or None, files=request.FILES or None, instance=clothes
    )
    formset = ColorFormset(
        request.POST or None,
        instance=clothes,
        initial=clothes.colors.order_by("pk").all(),
    )

    if request.method == "POST" and form.is_valid() and formset.is_valid():
        saved_clothes = form.save()
        x = float(request.POST.get("x"))
        y = float(request.POST.get("y"))
        w = float(request.POST.get("width"))
        h = float(request.POST.get("height"))

        if x != 0 and y != 0 and w != 0 and h != 0:
            saved_clothes.crop_picture(x, y, w, h)
            saved_clothes.extract_color()

        messages.info(
            request, f"Updated {saved_clothes.name} successfully.",
        )
        # for instance in formset.save(commit=False):
        #     # ... do something with m2m relationships ...

        # Save the order of a formset
        for ordered_form in formset.ordered_forms:
            ordered_form.instance.order = ordered_form.cleaned_data["ORDER"]
            ordered_form.instance.save()
        # return redirect("closet:edit_clothes", pk=pk)
        return redirect("closet:clothes")

    context = {
        "form": form,
        "formset": formset,
        "clothes": clothes,
        "add_or_edit": "Edit",
    }

    return render(request, "closet/add_clothes.html", context)


class UserClothes(LoginRequiredMixin, generic.ListView):
    template_name = "closet/clothes_list.html"

    def post(self, request):
        clothes_pks = request.POST.getlist("delete")
        Clothes.objects.filter(pk__in=clothes_pks).delete()
        return redirect("closet:clothes")

    def get_queryset(self):
        return self.request.user.clothes.order_by("-id").all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["who"] = self.request.user.username
        return context


class PublishedClothes(generic.DetailView):
    model = User
    template_name = "closet/clothes_list.html"

    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.kwargs["username"])
        context["object_list"] = user.clothes.filter(publish=True).all()
        context["who"] = self.kwargs["username"]
        return context


# class EditClothes(LoginRequiredMixin, generic.UpdateView):
#     model = Clothes
#     form_class = ClothesCreateForm
#     template_name = "closet/add_clothes.html"
#
#     def form_valid(self, form):
#         clothes = form.save()
#
#         x = float(self.request.POST.get("x"))
#         y = float(self.request.POST.get("y"))
#         w = float(self.request.POST.get("width"))
#         h = float(self.request.POST.get("height"))
#
#         clothes.crop_picture(x, y, w, h)
#         clothes.extract_color()
#
#         messages.info(
#             self.request,
#             f"{clothes.owner.username} updated {clothes.name} successfully.",
#         )
#         return redirect("closet:clothes")
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["add_or_edit"] = "Edit"
#         return context


class CreateOutfit(LoginRequiredMixin, generic.CreateView):
    model = Outfit
    form_class = OutfitCreateForm
    template_name = "closet/set_outfit.html"

    def get_form_kwargs(self):
        kwargs = super(CreateOutfit, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    # Add user and date created for an outfit
    def form_valid(self, form):
        outfit = form.save(commit=False)
        user = self.request.user
        outfit.owner = user
        outfit.created_at = timezone.now()

        if not outfit.name:
            count_outfit = user.outfits.count()
            outfit.name = f"Outfit {count_outfit + 1}"
        outfit.save()
        return redirect("closet:outfits")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["set_or_edit"] = "Set"
        return context


class UserOutfits(LoginRequiredMixin, generic.ListView):
    template_name = "closet/outfits_list.html"

    def get_queryset(self):
        return self.request.user.outfits.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["who"] = self.request.user.username
        return context


class PublishedOutfits(generic.DetailView):
    model = User
    template_name = "closet/outfits_list.html"

    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.kwargs["username"])
        context["object_list"] = user.outfits.filter(publish=True).all()
        context["who"] = self.kwargs["username"]
        return context


class EditOutfit(LoginRequiredMixin, generic.UpdateView):
    model = Outfit
    form_class = OutfitCreateForm
    success_url = reverse_lazy("closet:outfits")
    template_name = "closet/set_outfit.html"

    def get_form_kwargs(self):
        kwargs = super(EditOutfit, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["set_or_edit"] = "Edit"
        return context


def ajax_get_category(request):
    pk = request.GET.get("pk")
    # Return all categories if pk is None or empty.
    if not pk:
        category_list = Category.objects.all()

    # Return categories if geting its pk
    else:
        category_list = Category.objects.filter(parent__pk=pk)

    # Return a list that has dicts like this [ {'name': 'short sleeves', 'pk': '5'}, {'name': 'long sleeves', 'pk': '6'}, {...} ]
    category_list = [
        {"pk": category.pk, "name": category.name} for category in category_list
    ]

    # Return as JSON
    return JsonResponse({"categoryList": category_list})


def ajax_default_color(request, pk):
    if request.method == "POST":
        dic = QueryDict(request.body, encoding="utf-8")
        color_code = dic.get("color")
        id_name = dic.get("id_name")
        id = int(id_name.replace("color", "")) - 1

        clothes = Clothes.objects.get(pk=pk)
        color = clothes.colors.all()[id]
        color.code = color_code
        color.save()
    return JsonResponse({"colorCode": color_code})
