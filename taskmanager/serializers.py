"""Task Manger Serializer"""

from rest_framework import serializers
from taskmanager.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.

    This serializer converts the Task model instances into JSON format and vice versa,
    including fields such as title, description, and status_task.

    Fields:
        id (uuid.UUID): The unique identifier for the task.
        title (str): The title of the task.
        description (str): The description of the task.
        status_task (str): The status of the task. Choices are "TO DO", "IN PROGRESS", and "DONE".
        date_created (datetime): The timestamp when the task was created.
        last_updated (datetime): The timestamp when the task was last updated.
    """

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status_task",
            "date_created",
            "last_updated",
        ]
        read_only_fields = ["id", "date_created", "last_updated"]

    def validate_status_task(self, value):
        """
        Validate the status_task field to ensure it is one of the allowed choices.

        Args:
            value (str): The value of the status_task field.

        Returns:
            str: The validated value.

        Raises:
            serializers.ValidationError: If the value is not one of the allowed choices.
        """
        allowed_statuses = [choice[0] for choice in Task.TASK_STATUS]
        if value not in allowed_statuses:
            raise serializers.ValidationError(
                f"Invalid status: {value}. Must be one of {allowed_statuses}."
            )
        return value
