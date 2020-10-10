from django.urls import path
from . import views

app_name = "closet"

urlpatterns = [
    path("clothes/", views.UserClothes.as_view(), name="clothes"),
    path("clothes/add", views.CreateClothes.as_view(), name="add"),
    path("clothes/<int:pk>/edit", views.EditClothes.as_view(), name="edit_clothes"),
    path(
        "clothes/<slug:username>/",
        views.PublishedClothes.as_view(),
        name="user_clothes",
    ),
    path("clothes/<int:pk>/color/", views.ModifyColor.as_view(), name="clothes_color"),
    path("outfit/", views.UserOutfits.as_view(), name="outfits"),
    path("outfit/set", views.CreateOutfit.as_view(), name="set"),
    path("outfit/<int:pk>/edit", views.EditOutfit.as_view(), name="edit_outfit"),
    path(
        "outfit/<slug:username>/",
        views.PublishedOutfits.as_view(),
        name="user_outfits",
    ),
    path("api/get/category/", views.ajax_get_category, name="ajax_get_category"),
]
