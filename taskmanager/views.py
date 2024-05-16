"""Task Manager APIs"""

import uuid

from rest_framework import generics, status
from rest_framework.response import Response

from taskmanager.services import TaskService


task_service = TaskService()


class CreateTaskAPI(generics.GenericAPIView):
    """
    Endpoint for creating a new task.

    URL: /tasks/
    """

    def post(self, request):
        """
        Accepts POST requests with task data including title, description, and status_task.

        Returns:
            - HTTP 201 Created: If the task creation is successful.
        """
        return Response(
            data=task_service.create_task(
                title=request.data.get("title"),
                description=request.data.get("description"),
            ),
            status=status.HTTP_201_CREATED,
        )


class RetrieveUpdateDeleteTaskAPI(generics.GenericAPIView):
    """
    Endpoint for retrieving, updating, and deleting a task.

    URL: /tasks/<uuid:task_id>/
    """

    def get(self, request, task_id: uuid.UUID):
        """
        Accepts GET requests to retrieve task data by task ID.

        Returns:
            - HTTP 200 OK: If the task is found.
            - HTTP 404 Not Found: If the task does not exist.
        """
        return Response(
            data=task_service.get_task(task_id),
            status=status.HTTP_200_OK,
        )

    def put(self, request, task_id: uuid.UUID):
        """
        Accepts PUT requests with updated task data including title, description, and status_task.

        Returns:
            - HTTP 200 OK: If the task update is successful.
            - HTTP 404 Not Found: If the task does not exist.
        """
        return Response(
            data=task_service.update_task(
                task_id,
                title=request.data.get("title"),
                description=request.data.get("description"),
                status_task=request.data.get("status_task"),
            ),
            status=status.HTTP_200_OK,
        )

    def delete(self, request, task_id: uuid.UUID):
        """
        Accepts DELETE requests to delete a task by task ID.

        Returns:
            - HTTP 204 No Content: If the task deletion is successful.
            - HTTP 404 Not Found: If the task does not exist.
        """
        return Response(
            data=task_service.delete_task(task_id), status=status.HTTP_204_NO_CONTENT
        )


class ListTasksAPI(generics.GenericAPIView):
    """
    Endpoint for listing all tasks.

    URL: /tasks/
    """

    def get(self, request):
        """
        Accepts GET requests to retrieve a list of tasks.

        Returns:
            - HTTP 200 OK: With a paginated list of tasks.
        """
        return Response(
            data=task_service.list_tasks(request),
            status=status.HTTP_200_OK,
        )
