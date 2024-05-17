"""Task Manager Services"""

import uuid
from typing import Optional

from asgiref.sync import async_to_sync

from taskmanager import events
from taskmanager.models import Task
from taskmanager.serializers import TaskSerializer
from taskmaster.utils import get_object_or_error, paginate_queryset, remove_none_values


class TaskService:
    """
    Service class for task management.

    This class provides static methods for creating, retrieving, updating, and deleting tasks.
    It interacts with serializers and utility functions to perform these actions.

    Methods:
        create_task: Creates a new task with the provided data.
        get_task: Retrieves a task based on the task ID.
        list_tasks: Retrieves a paginated list of all tasks.
        update_task: Updates task information based on the provided data.
        delete_task: Deletes a task based on the task ID.
    """

    @staticmethod
    def create_task(
        user_id: uuid.UUID, title: str, description: Optional[str] = ""
    ) -> dict:
        """
        Creates a new task with the provided data.

        Args:
            user_id (uuid.UUID): Task owner
            title (str): The title of the task.
            description (str, optional): The description of the task.

        Returns:
            dict: Serialized task data.
        """
        task_data = {"user": user_id, "title": title, "description": description}
        serializer = TaskSerializer(data=task_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Strem task to WebSocket handler
        async_to_sync(events.send_task)(
            group_name="task_stream",
            data=serializer.data,
        )

        return serializer.data

    @staticmethod
    def get_task(user_id: uuid.UUID, task_id: str) -> dict:
        """
        Retrieves a task based on the task ID.

        Args:
            user_id (uuid.UUID): Task owner
            task_id (str): The ID of the task.

        Returns:
            dict: Serialized task data.
        """
        task = get_object_or_error(Task, id=task_id, user_id=user_id)
        return TaskSerializer(task).data

    @staticmethod
    def list_tasks(
        request, user_id: uuid.UUID, page: int = 1, page_size: int = 10
    ) -> dict:
        """
        Retrieves a paginated list of all tasks.

        Args:
            request (HttpRequest): The HTTP request object.
            user_id (uuid.UUID): Task owner
            page (int, optional): The page number for pagination.
            page_size (int, optional): The number of tasks per page.

        Returns:
            dict: Serialized task data in a paginated format.
        """
        tasks = Task.objects.filter(user_id=user_id)
        paginated_data = paginate_queryset(
            request=request,
            queryset=tasks,
            serializer_class=TaskSerializer,
            page=page,
            page_size=page_size,
        )
        return paginated_data.data

    @staticmethod
    def update_task(
        user_id: uuid.UUID,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status_task: Optional[str] = None,
    ) -> dict:
        """
        Updates task information based on the provided data.

        Args:
            user_id (uuid.UUID): Task owner
            task_id (str): The ID of the task.
            title (str, optional): The updated title of the task.
            description (str, optional): The updated description of the task.
            status_task (str, optional): The updated status of the task.

        Returns:
            dict: Serialized updated task data.
        """
        task = get_object_or_error(Task, id=task_id, user_id=user_id)
        task_update_data = remove_none_values(
            {
                "title": title,
                "description": description,
                "status_task": status_task,
            }
        )
        serializer = TaskSerializer(task, data=task_update_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    @staticmethod
    def delete_task(user_id: uuid.UUID, task_id: str) -> None:
        """
        Deletes a task based on the task ID.

        Args:
            user_id (uuid.UUID): Task owner
            task_id (str): The ID of the task to be deleted.
        """
        task = get_object_or_error(Task, id=task_id, user_id=user_id)
        task.delete()
        return {"message": "Task deleted successfully"}
