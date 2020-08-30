from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from .forms import UserCreateForm, ProfileForm
from .models import User, Profile

# Create your views here.
class SignUp(generic.CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"


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
        return self.request.user.followings.all()

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
    profile, x = Profile.objects.get_or_create(user=user)
    form = ProfileForm(request.POST or None, instance=profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("accounts:current")
    return render(request, "accounts/edit_profile.html", {"form": form})
