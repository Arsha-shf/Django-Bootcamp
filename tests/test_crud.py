import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from todos.models import Task


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="pass1234")


@pytest.fixture
def other_user(db):
    return User.objects.create_user(username="otheruser", password="pass1234")


@pytest.fixture
def task(user):
    return Task.objects.create(title="Test Task", description="Test desc", user=user)


@pytest.fixture
def logged_in_client(client, user):
    client.login(username="testuser", password="pass1234")
    return client


@pytest.mark.django_db
class TestCreateTaskView:

    def test_create_page_renders(self, logged_in_client):
        response = logged_in_client.get(reverse("create-task"))
        assert response.status_code == 200

    def test_create_uses_correct_template(self, logged_in_client):
        response = logged_in_client.get(reverse("create-task"))
        assert "todos/create_task.html" in [t.name for t in response.templates]

    def test_create_requires_login(self, client):
        response = client.get(reverse("create-task"))
        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_create_task_saves_to_db(self, logged_in_client):
        logged_in_client.post(reverse("create-task"), {
            "title": "New Task",
            "description": "Some description",
        })
        assert Task.objects.filter(title="New Task").exists()

    def test_create_task_assigns_to_logged_in_user(self, logged_in_client, user):
        logged_in_client.post(reverse("create-task"), {
            "title": "My Task",
            "description": "",
        })
        task = Task.objects.get(title="My Task")
        assert task.user == user

    def test_create_task_redirects_after_save(self, logged_in_client):
        response = logged_in_client.post(reverse("create-task"), {
            "title": "Redirect Task",
            "description": "",
        })
        assert response.status_code == 302
        assert response.url == reverse("task-list")

    def test_create_task_without_title_fails(self, logged_in_client):
        response = logged_in_client.post(reverse("create-task"), {
            "title": "",
            "description": "No title here",
        })
        assert response.status_code == 200
        assert not Task.objects.filter(description="No title here").exists()

    def test_create_task_without_description_succeeds(self, logged_in_client):
        logged_in_client.post(reverse("create-task"), {
            "title": "No Desc Task",
            "description": "",
        })
        assert Task.objects.filter(title="No Desc Task").exists()

    def test_create_task_title_too_long_fails(self, logged_in_client):
        response = logged_in_client.post(reverse("create-task"), {
            "title": "a" * 101,
            "description": "",
        })
        assert response.status_code == 200
        assert not Task.objects.filter(title="a" * 101).exists()


@pytest.mark.django_db
class TestEditTaskView:

    def test_edit_page_renders(self, logged_in_client, task):
        response = logged_in_client.get(reverse("edit-task", args=[task.id]))
        assert response.status_code == 200

    def test_edit_uses_correct_template(self, logged_in_client, task):
        response = logged_in_client.get(reverse("edit-task", args=[task.id]))
        assert "todos/edit_task.html" in [t.name for t in response.templates]

    def test_edit_requires_login(self, client, task):
        response = client.get(reverse("edit-task", args=[task.id]))
        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_edit_task_saves_changes(self, logged_in_client, task):
        logged_in_client.post(reverse("edit-task", args=[task.id]), {
            "title": "Updated Title",
            "description": "Updated desc",
        })
        task.refresh_from_db()
        assert task.title == "Updated Title"
        assert task.description == "Updated desc"

    def test_edit_task_redirects_after_save(self, logged_in_client, task):
        response = logged_in_client.post(reverse("edit-task", args=[task.id]), {
            "title": "Updated Title",
            "description": "",
        })
        assert response.status_code == 302
        assert response.url == reverse("task-list")

    def test_edit_task_form_prefilled(self, logged_in_client, task):
        response = logged_in_client.get(reverse("edit-task", args=[task.id]))
        assert b"Test Task" in response.content

    def test_cannot_edit_other_users_task(self, logged_in_client, other_user):
        other_task = Task.objects.create(
            title="Other Task",
            user=other_user
        )
        response = logged_in_client.get(reverse("edit-task", args=[other_task.id]))
        assert response.status_code == 404

    def test_edit_task_without_title_fails(self, logged_in_client, task):
        response = logged_in_client.post(reverse("edit-task", args=[task.id]), {
            "title": "",
            "description": "some desc",
        })
        assert response.status_code == 200
        task.refresh_from_db()
        assert task.title == "Test Task"

    def test_cannot_edit_other_users_task_via_post(self, logged_in_client, other_user):
        other_task = Task.objects.create(title="Other Task", user=other_user)
        response = logged_in_client.post(reverse("edit-task", args=[other_task.id]), {
            "title": "Hacked Title",
            "description": "",
        })
        assert response.status_code == 404
        other_task.refresh_from_db()
        assert other_task.title == "Other Task"

@pytest.mark.django_db
class TestDeleteTaskView:

    def test_delete_page_renders(self, logged_in_client, task):
        response = logged_in_client.get(reverse("delete-task", args=[task.id]))
        assert response.status_code == 200

    def test_delete_uses_correct_template(self, logged_in_client, task):
        response = logged_in_client.get(reverse("delete-task", args=[task.id]))
        assert "todos/delete_task.html" in [t.name for t in response.templates]

    def test_delete_requires_login(self, client, task):
        response = client.get(reverse("delete-task", args=[task.id]))
        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_delete_task_removes_from_db(self, logged_in_client, task):
        task_id = task.id
        logged_in_client.post(reverse("delete-task", args=[task.id]))
        assert not Task.objects.filter(id=task_id).exists()

    def test_delete_task_redirects_after_delete(self, logged_in_client, task):
        response = logged_in_client.post(reverse("delete-task", args=[task.id]))
        assert response.status_code == 302
        assert response.url == reverse("task-list")

    def test_cannot_delete_other_users_task(self, logged_in_client, other_user):
        other_task = Task.objects.create(
            title="Other Task",
            user=other_user
        )
        response = logged_in_client.post(reverse("delete-task", args=[other_task.id]))
        assert response.status_code == 404
        assert Task.objects.filter(id=other_task.id).exists()

    def test_delete_get_does_not_delete(self, logged_in_client, task):
        logged_in_client.get(reverse("delete-task", args=[task.id]))
        assert Task.objects.filter(id=task.id).exists()


@pytest.mark.django_db
class TestToggleTaskView:

    def test_toggle_marks_task_done(self, logged_in_client, task):
        assert not task.is_done
        logged_in_client.post(reverse("toggle-task", args=[task.id]))
        task.refresh_from_db()
        assert task.is_done

    def test_toggle_marks_task_undone(self, logged_in_client, task):
        task.is_done = True
        task.save()
        logged_in_client.post(reverse("toggle-task", args=[task.id]))
        task.refresh_from_db()
        assert not task.is_done

    def test_toggle_redirects_to_task_list(self, logged_in_client, task):
        response = logged_in_client.post(reverse("toggle-task", args=[task.id]))
        assert response.status_code == 302
        assert response.url == reverse("task-list")

    def test_toggle_requires_login(self, client, task):
        response = client.post(reverse("toggle-task", args=[task.id]))
        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_cannot_toggle_other_users_task(self, logged_in_client, other_user):
        other_task = Task.objects.create(
            title="Other Task",
            user=other_user
        )
        response = logged_in_client.post(reverse("toggle-task", args=[other_task.id]))
        assert response.status_code == 404

    def test_toggle_via_get_not_allowed(self, logged_in_client, task):
        logged_in_client.get(reverse("toggle-task", args=[task.id]))
        task.refresh_from_db()
        assert not task.is_done
