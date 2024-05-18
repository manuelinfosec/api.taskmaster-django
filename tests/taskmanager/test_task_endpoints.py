"""Test task endpoints"""

import pytest
from django.urls import reverse
from rest_framework import status

from taskmanager.models import Task
from tests.factories import TaskFactory

# Mark the entire test class to use Django DB and transactions
pytestmark = pytest.mark.django_db(transaction=True)


class TestTaskEndpoints:
    """
    Test suite for task-related API endpoints.
    Each test case uses fixtures from the `tests/factories` module.
    """

    def test_retrieve_task(self, api_client, task, created_user):
        """
        Test retrieving a specific task.

        Input parameters:
            api_client: A fixture that provides an instance of Django's test client.
            task: A fixture from `tests/factories` that creates a task instance.
            created_user: A fixture that provides a tuple with a user and its plain password.
        """
        # URL to retrieve a specific task
        url = reverse("retrieve_update_delete_task", args=[task.id])

        # Get the created user and authenticate the API client
        user, _ = created_user
        api_client.force_authenticate(user=user)

        # Send a GET request to retrieve the task
        response = api_client.get(url)

        # Assertions to check if the task was retrieved successfully
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == task.title
        assert response.data["description"] == task.description

    def test_update_task(self, api_client, task, created_user):
        """
        Test updating a specific task.

        Input parameters:
            api_client: A fixture that provides an instance of Django's test client.
            task: A fixture from `tests/factories` that creates a task instance.
            created_user: A fixture that provides a tuple with a user and its plain password.
        """
        # URL to update a specific task
        url = reverse("retrieve_update_delete_task", args=[task.id])
        data = {
            "title": "Updated Task",
            "description": "Updated Task Description",
            "status_task": "DONE",
        }

        # Get the created user and authenticate the API client
        user, _ = created_user
        api_client.force_authenticate(user=user)

        # Send a PUT request to update the task
        response = api_client.put(url, data=data, format="json")

        # Assertions to check if the task was updated successfully
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == data["title"]
        assert response.data["description"] == data["description"]
        assert response.data["status_task"] == data["status_task"]

    def test_delete_task(self, api_client, task, created_user):
        """
        Test deleting a specific task.

        Input parameters:
            api_client: A fixture that provides an instance of Django's test client.
            task: A fixture from `tests/factories` that creates a task instance.
            created_user: A fixture that provides a tuple with a user and its plain password.
        """
        # URL to delete a specific task
        url = reverse("retrieve_update_delete_task", args=[task.id])

        # Get the created user and authenticate the API client
        user, _ = created_user
        api_client.force_authenticate(user=user)

        # Send a DELETE request to delete the task
        response = api_client.delete(url)

        # Assertions to check if the task was deleted successfully
        assert response.status_code == status.HTTP_200_OK
        assert not Task.objects.filter(id=task.id).exists()

    def test_list_tasks(self, api_client, created_user):
        """
        Test listing all tasks for a user.

        Input parameters:
            api_client: A fixture that provides an instance of Django's test client.
            created_user: A fixture that provides a tuple with a user and its plain password.
        """
        # Get the created user
        user, _ = created_user

        # Create multiple tasks for the user
        tasks = TaskFactory.create_batch(3, user=user)

        # URL to list all tasks
        url = reverse("list_tasks")
        api_client.force_authenticate(user=user)

        # Send a GET request to list all tasks
        response = api_client.get(url)

        # Assertions to check if the tasks were listed successfully
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == len(tasks)
