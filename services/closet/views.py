from django.shortcuts import render
from django.views import generic
from .forms import ClothesCreateForm
from .models import ParentCategory, Category, Clothes
from django.urls import reverse_lazy
from django.http import JsonResponse

# Create your views here.


class ClothesCreate(generic.CreateView):
    model = Clothes
    form_class = ClothesCreateForm
    success_url = reverse_lazy("account:current")
    template_name = "closet/add_clothes.html"


def ajax_get_category(request):
    pk = request.GET.get("pk")
    # Return all categories if pk is None or empty.
    if not pk:
        category_list = Category.objects.all()

    # Return categories if geting its pk
    else:
        category_list = Category.objects.filter(parent__pk=pk)

    # Return a list that has dicts like this [ {'name': 'サッカー', 'pk': '3'}, {...}, {...} ]
    category_list = [
        {"pk": category.pk, "name": category.name} for category in category_list
    ]

    # Return as JSON
    return JsonResponse({"categoryList": category_list})
