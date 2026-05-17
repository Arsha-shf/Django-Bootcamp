import pytest
from django.contrib.auth.models import User
from todos.models import Task
import time


@pytest.mark.django_db
class TestTaskModel:

    def test_task_creation(self):
        user = User.objects.create_user(username="testuser", password="pass1234")
        task = Task.objects.create(
            title="Test Task",
            description="Test description",
            user=user
        )
        assert task.title == "Test Task"
        assert task.description == "Test description"
        assert not task.is_done
        assert task.user == user

    def test_task_str(self):
        user = User.objects.create_user(username="testuser2", password="pass1234")
        task = Task.objects.create(title="My Task", user=user)
        assert str(task) == "My Task"

    def test_task_default_is_done(self):
        user = User.objects.create_user(username="testuser3", password="pass1234")
        task = Task.objects.create(title="Another Task", user=user)
        assert not task.is_done

    def test_task_created_at_auto(self):
        user = User.objects.create_user(username="testuser4", password="pass1234")
        task = Task.objects.create(title="Timed Task", user=user)
        assert task.created_at is not None

    def test_task_description_optional(self):
        user = User.objects.create_user(username="testuser5", password="pass1234")
        task = Task.objects.create(title="No Desc Task", user=user)
        assert task.description == ""

    def test_task_deleted_when_user_deleted(self):
        user = User.objects.create_user(username="testuser6", password="pass1234")
        task = Task.objects.create(title="Cascade Task", user=user)
        task_id = task.id
        user.delete()
        assert not Task.objects.filter(id=task_id).exists()

    def test_task_updated_at_changes_on_save(self):
        user = User.objects.create_user(username="testuser7", password="pass1234")
        task = Task.objects.create(title="Update Test", user=user)
        first_updated = task.updated_at
        time.sleep(0.01)
        task.title = "Updated Title"
        task.save()
        task.refresh_from_db()
        assert task.updated_at > first_updated
