from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from .managers import CustomUserManager, InviteTokenManager, CompanyManager
from .settings import TOKEN_LENGTH

class Company(models.Model):
    """
    """
    name = models.CharField(max_length=30, default=None, unique=True)
    objects = CompanyManager()

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):

    username = None
    email = models.EmailField(('email address'), unique=True)
    company = models.ForeignKey(Company, default=None, null=True, blank=True, on_delete=models.DO_NOTHING)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    # def natural_key(self):
    #     return (self.email, None)

    def reset_password(self, password) -> None:
        self.set_password(password)
        self.save()


class InviteToken(models.Model):

    t_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, related_name="token_t_user")
    token = models.CharField(max_length=settings.LOGIN_TOKEN_LENGTH, default=None)
    date_created = models.DateTimeField(auto_now_add=True)
    objects = InviteTokenManager()

    class Meta:
        ordering = ["date_created"]

    def __str__(self):
        return "Token: " + str(self.token)
