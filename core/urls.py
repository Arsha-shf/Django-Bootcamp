import django.contrib.auth.urls
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tasks/", include("todos.urls")),
    path("accounts/", include(django.contrib.auth.urls)),
    path("", views.landing, name="landing"),
    path("accounts/register/", views.register, name="register"),
]

handler404 = "core.views.custom_404"