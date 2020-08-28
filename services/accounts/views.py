from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect, resolve_url
from . import models, forms


# Create your views here.
class SignUp(generic.CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"


class UserProfile(LoginRequiredMixin, generic.UpdateView):
    model = models.User
    form_class = forms.ProfileForm
    template_name = "accounts/user_profile.html"

    slug_field = "username"
    slug_url_kwarg = "username"

    def get_success_url(self):
        return resolve_url("accounts:profile", username=self.kwargs["username"])
