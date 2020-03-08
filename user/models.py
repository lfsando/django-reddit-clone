from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserProfile(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=20,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = "Usuário"


class UserSubscription(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="subscriptions",
                             verbose_name="Usuário")
    subreddit = models.ForeignKey("subreddit.Subreddit", on_delete=models.CASCADE, related_name="users",
                                  verbose_name="Subreddit")

    class Meta:
        verbose_name = "Inscrição"
        verbose_name_plural = "Inscrições"

    def __str__(self):
        return f"{self.user} • {self.subreddit}"
