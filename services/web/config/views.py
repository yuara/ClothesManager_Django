from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
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
        if Forecast.objects.first():
            user_pref_id = self.request.user.profile.prefecture.id
            user_forecast = (
                Forecast.objects.filter(prefecture=user_pref_id)
                .order_by("-created_at")
                .first()
            )
            user_clothes = Clothes.objects.select_related("parent_category").filter(
                category__in=user_forecast.clothes_index.categories.all()
            )
            context["outerwears"] = user_clothes.filter(parent_category_id=1)
            context["tops"] = user_clothes.filter(parent_category_id=2)
            context["bottoms"] = user_clothes.filter(parent_category_id=3)
            context["forecast"] = user_forecast
        return context
