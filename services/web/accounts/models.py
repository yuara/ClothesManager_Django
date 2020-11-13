import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
import uuid as uuid_lib

# Create your models here.
class Area(models.Model):
    name = models.CharField(_("area"), max_length=255)

    def __str__(self):
        return self.name


class Prefecture(models.Model):
    name = models.CharField(_("prefecture"), max_length=255)
    area = models.ForeignKey("Area", verbose_name="area", on_delete=models.PROTECT)

    def __str__(self):
        return self.name


def set_random_color():
    return "%06x" % random.randint(0, 0xFFFFFF)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    about_me = models.TextField(blank=True)
    webpage = models.URLField(blank=True)
    area = models.ForeignKey(Area, on_delete=models.PROTECT, blank=True, default=1)
    prefecture = models.ForeignKey(
        Prefecture, on_delete=models.PROTECT, blank=True, default=1
    )
    picture = models.ImageField(upload_to="profile_pic/", blank=True)
    color = models.CharField(max_length=6, blank=True, default=set_random_color)

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"

    def __str__(self):
        return f"{self.user.username}'s profile"


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

    following = models.ManyToManyField(
        "self", related_name="followers", blank=True, symmetrical=False
    )
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
            self.following.add(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        return user in self.following.all()
