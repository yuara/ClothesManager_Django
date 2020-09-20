from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from .forms import UserChangeForm, ProfileForm
from .models import User, Profile

# Register your models here.


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


# class FollowingInline(admin.StackedInline):
#     model = FollowUser
#     fk_name = "following"
#     extra = 1
#
#
# class FollowerInline(admin.StackedInline):
#     model = FollowUser
#     fk_name = "follower"
#     extra = 1
#


@admin.register(User)
class AdminUserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    form = UserChangeForm
    model = get_user_model()

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("full_name", "email")},),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        ("Following / Followers", {"fields": ("following", "followers")}),
    )
    list_display = (
        "username",
        "email",
        "full_name",
        "is_staff",
    )
    search_fields = ("username", "full_name", "email")
    filter_horizontal = ("groups", "user_permissions", "following", "followers")


admin.site.register(Profile)
