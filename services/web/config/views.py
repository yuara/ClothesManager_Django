from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView
from accounts.models import Profile
from closet.models import Clothes, Forecast, Outfit
from django.shortcuts import render


class HomePage(TemplateView):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        print("IP Address for debug-toolbar: " + request.META["REMOTE_ADDR"])
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        messages.info(
            self.request, f"You can try a demo with username: yu, password: yuarakawa.",
        )
        return super().get(request, *args, **kwargs)


@login_required
def index(request):
    user = request.user
    # profile, is_created = Profile.objects.get_or_create(user=user)
    user_pref_id = user.profile.prefecture.id
    user_forecast = (
        Forecast.objects.filter(prefecture=user_pref_id).order_by("-created_at").first()
    )
    context = {}

    if user_forecast:
        context["forecast"] = user_forecast

        forecast_categories = user_forecast.clothes_index.categories.all()
        context["outerwears"] = forecast_categories.filter(parent_id=1)
        context["tops"] = forecast_categories.filter(parent_id=2)
        context["bottoms"] = forecast_categories.filter(parent_id=3)

        user_categories = Clothes.objects.select_related("parent_category").filter(
            category__in=forecast_categories
        )
        context["user_outerwears"] = user_categories.filter(parent_category_id=1)
        context["user_tops"] = user_categories.filter(parent_category_id=2)
        context["user_bottoms"] = user_categories.filter(parent_category_id=3)

    if request.method == "POST":
        clothes_id = []
        for x in request.POST:
            if x[0] == "#":
                clothes_id.append(request.POST[x])
        # TODO: Create validation for a combination of clothes on index page
        if len(clothes_id) == 2:
            a = Outfit.objects.create(
                owner=user, top_id=clothes_id[0], bottom_id=clothes_id[1]
            )
            a.set_name()
            a.save()
            msg = f"Saved {a.name} successfully."
        elif len(clothes_id) == 3:
            a = Outfit.objects.create(
                owner=user,
                outerwear_id=clothes_id[0],
                top_id=clothes_id[1],
                bottom_id=clothes_id[2],
            )
            a.set_name()
            a.save()
            msg = f"Saved {a.name} successfully."
        else:
            msg = f"Failed to set an outfit"

        messages.info(
            request, msg,
        )

    if is_created == True:
        messages.info(request, "Edit your profile to change your location")

    return render(request, "index.html", context)
