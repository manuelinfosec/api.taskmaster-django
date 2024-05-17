"""Test task endpoints"""

import pytest
from rest_framework import status
from django.urls import reverse

from taskmanager.models import Task
from tests.factories import TaskFactory


# Mark the entire test class to use Django DB and transactions
pytestmark = pytest.mark.django_db(transaction=True)


class TestTaskEndpoints:

    def test_retrieve_task(self, api_client, task):
        url = reverse("retrieve_update_delete_task", args=[task.id])
        response = api_client().get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == task.title
        assert response.data["description"] == task.description

    def test_update_task(self, api_client, task):
        url = reverse("retrieve_update_delete_task", args=[task.id])
        data = {
            "title": "Updated Task",
            "description": "Updated Task Description",
            "status_task": "completed",
        }
        response = api_client().put(url, data=data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == data["title"]
        assert response.data["description"] == data["description"]
        assert response.data["status_task"] == data["status_task"]

    def test_delete_task(self, api_client, task):
        url = reverse("retrieve_update_delete_task", args=[task.id])
        response = api_client().delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Task.objects.filter(id=task.id).exists()

    def test_list_tasks(self, api_client, user):
        # Create multiple tasks for the user
        tasks = TaskFactory.create_batch(3, user=user)

        url = reverse("list_tasks")
        response = api_client().get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == len(tasks)
