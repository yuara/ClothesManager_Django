from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("users/", views.Users.as_view(), name="all"),
    path("profile/", views.CurrentUserProfile.as_view(), name="current"),
    path("profile/<slug:username>", views.UserProfile.as_view(), name="profile"),
    # path("profile/<slug:username>/edit", views.EditProfile.as_view(), name="edit"),
    path("profile/<slug:username>/edit", views.update_user, name="edit"),
    path("follow/<slug:username>", views.follow, name="follow"),
    path("unfollow/<slug:username>", views.unfollow, name="unfollow"),
    path("follower", views.Followers.as_view(), name="followers"),
    path("following", views.FollowingUsers.as_view(), name="followings"),
]
