import pytest
from django.core.exceptions import ValidationError
from taskmanager.models import Task


@pytest.mark.django_db
class TestTaskModel:
    """
    Test suite for the Task model.
    Each test case uses fixtures from the `tests/factories` module.
    """

    def test_create_task(self, user_factory):
        """
        Test creating a task with valid data.
        Input parameter:
            user_factory: A fixture from `tests/factories` that creates user instances.
        """
        # Create a user using the user factory
        user = user_factory.create()

        # Create a task associated with the user
        task = Task.objects.create(
            user=user,
            title="Sample Task",
            description="This is a sample task.",
            status_task="TO DO",
        )

        # Assertions to check if the task was created correctly
        assert task.title == "Sample Task"
        assert task.description == "This is a sample task."
        assert task.status_task == "TO DO"
        assert task.user == user

    def test_task_string_representation(self, task_factory):
        """
        Test the string representation of a task.
        Input parameter:
            task_factory: A fixture from `tests/factories` that creates task instances.
        """
        # Create a task with a specific title
        task = task_factory.create(title="Sample Task")

        # Assert that the string representation of the task matches the title
        assert str(task) == "Sample Task"

    def test_task_status_choices(self, task_factory):
        """
        Test that only valid status choices can be assigned to a task.
        Input parameter:
            task_factory: A fixture from `tests/factories` that creates task instances.
        """
        # Create a task with a valid status
        task = task_factory.create(status_task="IN PROGRESS")

        # Assert the task has the correct status
        assert task.status_task == "IN PROGRESS"

        # Attempt to set an invalid status and check for a validation error
        with pytest.raises(ValidationError):
            task.status_task = "INVALID STATUS"
            task.save()

    def test_update_task(self, task_factory):
        """
        Test updating a task's title.
        Input parameter:
            task_factory: A fixture from `tests/factories` that creates task instances.
        """
        # Create a task
        task = task_factory.create()

        # Update the task's title
        new_title = "Updated Task"
        task.title = new_title
        task.save()

        # Retrieve the updated task and assert the title was updated correctly
        updated_task = Task.objects.get(id=task.id)
        assert updated_task.title == new_title

    def test_delete_task(self, task_factory):
        """
        Test deleting a task.
        Input parameter:
            task_factory: A fixture from `tests/factories` that creates task instances.
        """
        # Create a task
        task = task_factory.create()
        task_id = task.id

        # Delete the task
        task.delete()

        # Assert that the task no longer exists
        with pytest.raises(Task.DoesNotExist):
            Task.objects.get(id=task_id)

    def test_task_default_status(self, task_factory):
        """
        Test that a task has the default status 'TO DO' when created.
        Input parameter:
            task_factory: A fixture from `tests/factories` that creates task instances.
        """
        # Create a task
        task = task_factory.create()

        # Assert that the default status is 'TO DO'
        assert task.status_task == "TO DO"
