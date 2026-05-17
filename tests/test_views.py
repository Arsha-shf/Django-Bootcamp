import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from todos.models import Task


@pytest.mark.django_db
class TestLandingView:

    def test_landing_redirects_authenticated_user(self, client):
        User.objects.create_user(username="testuser", password="pass1234")
        client.login(username="testuser", password="pass1234")
        response = client.get(reverse("landing"))
        assert response.status_code == 302
        assert response.url == "/tasks/"

    def test_landing_renders_for_anonymous(self, client):
        response = client.get(reverse("landing"))
        assert response.status_code == 200

    def test_landing_uses_correct_template(self, client):
        response = client.get(reverse("landing"))
        assert "landing.html" in [t.name for t in response.templates]


@pytest.mark.django_db
class TestTaskListView:

    def test_task_list_requires_login(self, client):
        response = client.get(reverse("task-list"))
        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_task_list_renders_for_logged_in_user(self, client):
        User.objects.create_user(username="testuser", password="pass1234")
        client.login(username="testuser", password="pass1234")
        response = client.get(reverse("task-list"))
        assert response.status_code == 200

    def test_task_list_uses_correct_template(self, client):
        User.objects.create_user(username="testuser", password="pass1234")
        client.login(username="testuser", password="pass1234")
        response = client.get(reverse("task-list"))
        assert "todos/task_list.html" in [t.name for t in response.templates]

    def test_task_list_shows_only_user_tasks(self, client):
        user1 = User.objects.create_user(username="user1", password="pass1234")
        user2 = User.objects.create_user(username="user2", password="pass1234")
        Task.objects.create(title="User1 Task", user=user1)
        Task.objects.create(title="User2 Task", user=user2)
        client.login(username="user1", password="pass1234")
        response = client.get(reverse("task-list"))
        tasks = response.context["tasks"]
        assert tasks.count() == 1
        assert tasks.first().title == "User1 Task"

    def test_task_list_empty_for_new_user(self, client):
        User.objects.create_user(username="newuser", password="pass1234")
        client.login(username="newuser", password="pass1234")
        response = client.get(reverse("task-list"))
        assert response.context["tasks"].count() == 0


@pytest.mark.django_db
class TestRegisterView:

    def test_register_page_renders(self, client):
        response = client.get(reverse("register"))
        assert response.status_code == 200

    def test_register_uses_correct_template(self, client):
        response = client.get(reverse("register"))
        assert "registration/register.html" in [t.name for t in response.templates]

    def test_register_creates_user(self, client):
        client.post(reverse("register"), {
            "username": "newuser",
            "password1": "Str0ng!Pass99",
            "password2": "Str0ng!Pass99",
        })
        assert User.objects.filter(username="newuser").exists()

    def test_register_logs_in_after_signup(self, client):
        response = client.post(reverse("register"), {
            "username": "newuser",
            "password1": "Str0ng!Pass99",
            "password2": "Str0ng!Pass99",
        })
        assert response.status_code == 302
        assert response.url == "/tasks/"

    def test_register_with_mismatched_passwords(self, client):
        response = client.post(reverse("register"), {
            "username": "newuser",
            "password1": "Str0ng!Pass99",
            "password2": "WrongPass99!",
        })
        assert response.status_code == 200
        assert not User.objects.filter(username="newuser").exists()

    def test_register_redirects_authenticated_user(self, client):
        User.objects.create_user(username="existing", password="pass1234")
        client.login(username="existing", password="pass1234")
        response = client.get(reverse("register"))
        assert response.status_code == 302
        assert response.url == "/tasks/"


@pytest.mark.django_db
class TestLoginView:

    def test_login_page_renders(self, client):
        response = client.get(reverse("login"))
        assert response.status_code == 200

    def test_login_uses_correct_template(self, client):
        response = client.get(reverse("login"))
        assert "registration/login.html" in [t.name for t in response.templates]

    def test_login_with_valid_credentials(self, client):
        User.objects.create_user(username="testuser", password="pass1234")
        response = client.post(reverse("login"), {
            "username": "testuser",
            "password": "pass1234",
        })
        assert response.status_code == 302

    def test_login_with_invalid_credentials(self, client):
        response = client.post(reverse("login"), {
            "username": "ghost",
            "password": "wrongpass",
        })
        assert response.status_code == 200

    def test_login_redirects_to_tasks(self, client):
        User.objects.create_user(username="testuser", password="pass1234")
        response = client.post(reverse("login"), {
            "username": "testuser",
            "password": "pass1234",
        })
        assert response.url == "/tasks/"


@pytest.mark.django_db
class TestLogoutView:

    def test_logout_redirects_to_landing(self, client):
        User.objects.create_user(username="testuser", password="pass1234")
        client.login(username="testuser", password="pass1234")
        response = client.post(reverse("logout"))
        assert response.status_code == 302
        assert response.url == "/"

    def test_logout_actually_logs_out(self, client):
        User.objects.create_user(username="testuser", password="pass1234")
        client.login(username="testuser", password="pass1234")
        client.post(reverse("logout"))
        response = client.get(reverse("task-list"))
        assert response.status_code == 302
        assert "/accounts/login/" in response.url
