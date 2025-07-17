from django.urls import path

from users.views import main

urlpatterns = (path("", main, name="main"),)
