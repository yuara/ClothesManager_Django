from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
import random
from django.http import JsonResponse
from .forms import UserCreateForm, ProfileForm
from .models import User, Profile
from closet.models import Area, Prefecture

# Create your views here.
class SignUp(generic.CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        self.object = user = form.save()
        area = Area.objects.get(id=1)
        prefecture = Prefecture.objects.get(id=1)
        color = "%06x" % random.randint(0, 0xFFFFFF)
        profile = Profile.objects.create(
            user=user, area=area, prefecture=prefecture, color=color
        )
        messages.info(self.request, f"Sign Up! {user.username}!")
        return redirect(self.get_success_url())


class Users(generic.ListView):
    model = User
    template_name = "accounts/users_list.html"


class CurrentUserProfile(LoginRequiredMixin, generic.TemplateView):

    template_name = "accounts/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # はじめに継承元のメソッドを呼び出す
        context["user"] = self.request.user
        return context


class UserProfile(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = "accounts/user_profile.html"

    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.kwargs["username"])
        current_user = self.request.user
        if current_user != user:
            if current_user.is_following(user):
                context["is_following"] = True
            else:
                context["is_following"] = False
        return context


# class EditProfile(LoginRequiredMixin, generic.UpdateView):
#     model = User
#     form_class = ProfileForm
#     success_url = reverse_lazy("accounts:current")
#     template_name = "accounts/edit_profile.html"
#
#     slug_field = "username"
#     slug_url_kwarg = "username"


class FollowingUsers(LoginRequiredMixin, generic.ListView):

    template_name = "accounts/users_list.html"

    def get_queryset(self):
        return self.request.user.following.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["followers_or_following"] = "Following"
        return context


class Followers(LoginRequiredMixin, generic.ListView):

    template_name = "accounts/users_list.html"

    def get_queryset(self):
        return self.request.user.followers.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["followers_or_following"] = "Followers"
        return context


def follow(request, username):
    user = get_object_or_404(User, username=username)
    if user == request.user:
        return redirect("accounts:profile", username=username)
    request.user.follow(user)
    request.user.save()
    return redirect("accounts:profile", username=username)


def unfollow(request, username):
    user = get_object_or_404(User, username=username)
    if user == request.user:
        return redirect("accounts:profile", username=username)
    request.user.unfollow(user)
    request.user.save()
    return redirect("accounts:profile", username=username)


def update_user(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("accounts:current")
    form = ProfileForm(instance=profile)
    return render(
        request, "accounts/edit_profile.html", {"form": form, "profile": profile}
    )


def ajax_get_location(request):
    pk = request.GET.get("pk")
    # Return all categories if pk is None or empty.
    if not pk:
        pref_list = Prefecture.objects.all()

    # Return categories if geting its pk
    else:
        pref_list = Prefecture.objects.filter(parent__pk=pk)

    # Return a list that has dicts like this [ {'name': 'short sleeves', 'pk': '5'}, {'name': 'long sleeves', 'pk': '6'}, {...} ]
    pref_list = [
        {"pk": prefecture.pk, "name": prefecture.name} for prefecture in pref_list
    ]

    # Return as JSON
    return JsonResponse({"categoryList": pref_list})
