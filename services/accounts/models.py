from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
import uuid as uuid_lib

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    about_me = models.TextField(blank=True)
    webpage = models.URLField(blank=True)
    picture = models.ImageField(upload_to="accounts/profile_pic", blank=True)

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profile"

    def __str__(self):
        return f"{self.user.username}'s profile"


class FollowUser(models.Model):
    follower = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="following_followusers"
    )
    following = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="follower_followusers"
    )

    class Meta:
        unique_together = ("follower", "following")


class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(default=uuid_lib.uuid4, primary_key=True, editable=False)
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={"unique": _("A user with that username already exists."),},
    )
    full_name = models.CharField(_("your name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)

    followings = models.ManyToManyField(
        "User",
        verbose_name="following users",
        through="FollowUser",
        related_name="+",
        through_fields=("follower", "following"),
        blank=True,
    )
    followers = models.ManyToManyField(
        "User",
        verbose_name="followers",
        through="FollowUser",
        related_name="+",
        through_fields=("following", "follower"),
        blank=True,
    )

    clothings = models

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "email",
    ]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # Use full name and remove first and last name
    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name

    def follow(self, user):
        if not self.is_following(user):
            self.following_followusers.create(following=user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following_followusers.filter(following=user).delete()

    def is_following(self, user):
        return self.following_followusers.filter(following=user).count() > 0
