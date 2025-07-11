import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase


@pytest.mark.django_db
class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", password="foo")
        assert user.email == "normal@user.com"
        assert user.is_active == True
        assert user.is_staff == False
        assert user.is_superuser == False
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email="super@user.com", password="foo")
        assert admin_user.email == "super@user.com"
        assert admin_user.is_active == True
        assert admin_user.is_staff == True
        assert admin_user.is_superuser == True
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False
            )
