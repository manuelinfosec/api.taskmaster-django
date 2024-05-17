import pytest
from taskmanager.models import Task

# Mark the entire test class to use Django DB and transactions
pytestmark = pytest.mark.django_db(transaction=True)


@pytest.mark.django_db
class TestTaskModel:

    def test_create_task(self, user_factory):
        user = user_factory.build()
        task = Task.objects.create(
            user=user,
            title="Sample Task",
            description="This is a sample task.",
            status_task="TO DO",
        )
        assert task.title == "Sample Task"
        assert task.description == "This is a sample task."
        assert task.status_task == "TO DO"
        assert task.user == user

    def test_task_string_representation(self, task_factory):
        task = task_factory.create(title="Sample Task")
        assert str(task) == "Sample Task"

    def test_task_status_choices(self, task_factory):
        task = task_factory.create(status_task="IN PROGRESS")
        assert task.status_task == "IN PROGRESS"

        with pytest.raises(ValueError):
            task.status_task = "INVALID STATUS"
            task.save()

    def test_update_task(self, task_factory):
        task = task_factory.create()
        new_title = "Updated Task"
        task.title = new_title
        task.save()
        updated_task = Task.objects.get(id=task.id)
        assert updated_task.title == new_title

    def test_delete_task(self, task_factory):
        task = task_factory.create()
        task_id = task.id
        task.delete()
        with pytest.raises(Task.DoesNotExist):
            Task.objects.get(id=task_id)

    def test_task_default_status(self, task_factory):
        task = task_factory.create()
        assert task.status_task == "TO DO"
