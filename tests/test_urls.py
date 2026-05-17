from django.urls import reverse, resolve
from todos.views import task_list
from core.views import landing, register
from django.contrib.auth import views as auth_views


class TestUrls:

    def test_landing_url(self):
        url = reverse("landing")
        assert url == "/"

    def test_task_list_url(self):
        url = reverse("task-list")
        assert url == "/tasks/"

    def test_login_url(self):
        url = reverse("login")
        assert url == "/accounts/login/"

    def test_register_url(self):
        url = reverse("register")
        assert url == "/accounts/register/"

    def test_logout_url(self):
        url = reverse("logout")
        assert url == "/accounts/logout/"

    def test_task_list_resolves(self):
        resolver = resolve("/tasks/")
        assert resolver.func == task_list

    def test_landing_resolves(self):
        resolver = resolve("/")
        assert resolver.func == landing

    def test_register_resolves(self):
        resolver = resolve("/accounts/register/")
        assert resolver.func == register

    def test_login_resolves(self):
        resolver = resolve("/accounts/login/")
        assert resolver.func.view_class == auth_views.LoginView

    def test_logout_resolves(self):
        resolver = resolve("/accounts/logout/")
        assert resolver.func.view_class == auth_views.LogoutView
