from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .forms import ClothesCreateForm
from .models import ParentCategory, Category, Clothes
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils import timezone

# Create your views here.


class ClothesCreate(LoginRequiredMixin, generic.CreateView):
    model = Clothes
    form_class = ClothesCreateForm
    success_url = reverse_lazy("account:current")
    template_name = "closet/add_clothes.html"

    def form_valid(self, form):
        clothes = form.save(commit=False)
        clothes.owner = self.request.user
        clothes.created_at = timezone.now()
        clothes.save()
        return redirect("closet:add")


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
