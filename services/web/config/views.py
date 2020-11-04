from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView
from closet.models import Clothes, Forecast


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


class IndexPage(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_pref_id = self.request.user.profile.prefecture.id
        user_forecast = (
            Forecast.objects.filter(prefecture=user_pref_id)
            .order_by("-created_at")
            .first()
        )
        if user_forecast:
            context["forecast"] = user_forecast

            forecast_categories = user_forecast.clothes_index.categories.all()
            context["outerwears"] = forecast_categories.filter(parent_id=1)
            context["tops"] = forecast_categories.filter(parent_id=2)
            context["bottoms"] = forecast_categories.filter(parent_id=3)

            # TODO: j
            user_categories = Clothes.objects.select_related("parent_category").filter(
                category__in=forecast_categories
            )
            context["user_outerwears"] = user_categories.filter(parent_category_id=1)
            context["user_tops"] = user_categories.filter(parent_category_id=2)
            context["user_bottoms"] = user_categories.filter(parent_category_id=3)

        return context


def ajax_get_clothes(request):
    category_name = request.GET.get("category_name")
    category_name = category_name.replace("#", "").replace("-", " ").replace("-", " ")
    user = request.user
    if not category_name:
        clothes_dict = {"text": "Something is happening to get category name."}
        is_success = False

    else:
        clothes_list = Clothes.objects.filter(
            owner=user, category__name=category_name
        ).all()
        if clothes_list:
            clothes_dict = []
            for clothes in clothes_list:
                if clothes.picture:
                    img_url = clothes.picture.url
                else:
                    img_url = f"/static/img/icon/clothes/{clothes.category}.jpg"
                clothes_dict.append(
                    {"pk": clothes.pk, "name": clothes.name, "image": img_url}
                )
            is_success = True
        else:
            clothes_dict = {"text": "Not Registered Yet"}
            is_success = False

    return JsonResponse({"clothesDict": clothes_dict, "isSuccess": is_success})
