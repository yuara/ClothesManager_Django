from django.urls import path
from . import views

app_name = "ajax"

urlpatterns = [
    path("get/location/", views.get_location, name="get_location"),
    path("get/clothes/", views.get_clothes, name="get_clothes"),
    path("get/category/", views.get_category, name="get_category"),
    path("post/<int:pk>/color/", views.default_color, name="default_color"),
]
