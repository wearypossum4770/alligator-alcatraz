from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import BooleanField, CharField, DateTimeField, EmailField, Model
from django.utils import timezone

from users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = EmailField(unique=True)

    first_name = CharField(max_length=100, blank=False, null=False)

    middle_name = CharField(max_length=100, blank=True, null=True)

    last_name = CharField(max_length=100, blank=False, null=False)

    is_staff = BooleanField(default=False)

    is_active = BooleanField(default=True)

    date_joined = DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
