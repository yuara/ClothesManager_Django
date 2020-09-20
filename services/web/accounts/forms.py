from django.contrib.auth import get_user_model
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Profile


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Display name"
        self.fields["email"].label = "Email address"


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("about_me", "webpage", "picture")


class UserChangeForm(forms.ModelForm):

    following = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(verbose_name="Following", is_stacked=False),
    )

    followers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(verbose_name="Followers", is_stacked=False),
    )

    class Meta:
        model = get_user_model()
        # add 'following' and 'followers' to the fields:
        fields = ("following", "followers")

    # also needed to initialize properly:
    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)

        # Filter out the self user in the lists and initialize followers list:
        if self.instance and self.instance.pk:
            self.fields["following"] = forms.ModelMultipleChoiceField(
                queryset=User.objects.all().exclude(pk=self.instance.pk),
                required=False,
                widget=FilteredSelectMultiple(
                    verbose_name="Following", is_stacked=False
                ),
            )
            self.fields["followers"] = forms.ModelMultipleChoiceField(
                queryset=User.objects.all().exclude(pk=self.instance.pk),
                required=False,
                widget=FilteredSelectMultiple(
                    verbose_name="Followers", is_stacked=False
                ),
            )
            self.fields["followers"].initial = self.instance.followers.all()
