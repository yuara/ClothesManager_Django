from django.urls import path
from . import views

app_name = "closet"

urlpatterns = [
    path("clothes/", views.UserClothes.as_view(), name="clothes"),
    path("clothes/add", views.ClothesCreate.as_view(), name="add"),
    path("clothes/<int:pk>/edit", views.EditClothes.as_view(), name="edit_clothes"),
    path(
        "clothes/<slug:username>/", views.LimitedClothes.as_view(), name="user_clothes"
    ),
    path("api/category/get/", views.ajax_get_category, name="ajax_get_category"),
]
