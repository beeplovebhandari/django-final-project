from django.contrib.auth.validators import UnicodeUsernameValidator

from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from apps.commons.models import BaseModel


class User (AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        null=True, blank=True

        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(unique=True blank=True, null=True )
    middle_name = models.CharField(max_length=20, blank=True, null=True)
    account_activated = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

class UserAccountActivationKey (BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_activation_keys")
    key  = models.CharField(max_length=50)

class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.FileField(null=True, blank=True, upload_to='profile_pictures')
    phone_number = models.CharField(max_length=14)
    address = models.TextField(max_length=50)
    bio = models.TextField(max_length=1000)
    resume  =models.FileField(null=True, blank=True, upload_to='resumes')

    def __str__(self):
        return f"Profile of {self.user.email}"