from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .forms import ClothesCreateForm
from accounts.models import User
from .models import ParentCategory, Category, Clothes
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings

# Create your views here.


class ClothesCreate(LoginRequiredMixin, generic.CreateView):
    model = Clothes
    form_class = ClothesCreateForm
    template_name = "closet/add_clothes.html"

    # Add user and date created in a clothes
    def form_valid(self, form):
        clothes = form.save(commit=False)
        user = self.request.user
        clothes.owner = user
        clothes.created_at = timezone.now()

        if not clothes.name:
            category = clothes.category
            count_clothes = user.clothes.filter(category=category).count()
            clothes.name = f"{category} {count_clothes + 1}"
        clothes.save()
        return redirect("closet:clothes")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["add_or_edit"] = "Add"
        return context


class UserClothes(LoginRequiredMixin, generic.ListView):
    template_name = "closet/clothes_list.html"

    def get_queryset(self):
        return self.request.user.clothes.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["who"] = self.request.user.username
        return context


class LimitedClothes(generic.DetailView):
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


class EditClothes(LoginRequiredMixin, generic.UpdateView):
    model = Clothes
    form_class = ClothesCreateForm
    success_url = reverse_lazy("closet:clothes")
    template_name = "closet/add_clothes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["add_or_edit"] = "Edit"
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
