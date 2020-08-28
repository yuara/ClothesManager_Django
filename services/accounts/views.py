from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from . import models, forms

# Create your views here.
class SignUp(generic.CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"


class Users(generic.ListView):
    model = models.User
    template_name = "accounts/users_list.html"


class CurrentUserProfile(generic.TemplateView):

    template_name = "accounts/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # はじめに継承元のメソッドを呼び出す
        context["user"] = self.request.user
        return context


class UserProfile(generic.DetailView):
    model = models.User
    template_name = "accounts/user_profile.html"

    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = models.User.objects.get(username=self.kwargs["username"])
        current_user = self.request.user
        if current_user != user:
            if current_user.is_following(user):
                context["is_following"] = True
            else:
                context["is_following"] = False
        return context


class EditProfile(LoginRequiredMixin, generic.UpdateView):
    model = models.User
    form_class = forms.ProfileForm
    template_name = "accounts/edit_profile.html"

    slug_field = "username"
    slug_url_kwarg = "username"


class FollowingUsers(generic.ListView):

    template_name = "accounts/users_list.html"

    def get_queryset(self):
        return self.request.user.followings.all()


class Followers(generic.ListView):

    template_name = "accounts/users_list.html"

    def get_queryset(self):
        return self.request.user.followers.all()


def follow(request, username):
    user = get_object_or_404(models.User, username=username)
    if user == request.user:
        return redirect("accounts:profile", username=username)
    request.user.follow(user)
    request.user.save()
    return redirect("accounts:profile", username=username)


def unfollow(request, username):
    user = get_object_or_404(models.User, username=username)
    if user == request.user:
        return redirect("accounts:profile", username=username)
    request.user.unfollow(user)
    request.user.save()
    return redirect("accounts:profile", username=username)


#
# def update_user(request, username):
#     user = get_object_or_404(models.User, username=username)
#     if user.profile is None:
#         profile = models.Profile(user=user)
#     else:
#         profile = user.profile
#     user_form = forms.UserEditableForm(request.POST or None, instance=user)
#     profile_form = forms.ProfileForm(request.POST or None, instance=profile)
#     if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():
#         user_form.save()
#         profile_form.save()
#         return redirect("index")
#
#     context = {
#         "user_form": user_form,
#         "profile_form": profile_form,
#     }
#     return render(request, "accounts/edit_profile.html", context)
