from django.urls import path
from . import views

app_name = "closet"

urlpatterns = [
    path("", views.ClothesCreate.as_view(), name="add"),
    path("api/category/get/", views.ajax_get_category, name="ajax_get_category"),
]
