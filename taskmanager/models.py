"""Task manager models"""

from django.contrib.auth import get_user_model
from django.db import models

from taskmaster.utils import BaseModel


class Task(BaseModel):
    """
    Task model representing a task in the task management application.

    This model extends the BaseModel class to include additional fields
    for task management, such as title, description, and status.

    Attributes:
        TASK_STATUS (tuple): A tuple of possible task status choices.

        user (User): Task Owner. This is field is a foreign reference to the User model.
        title (str): The title of the task. This field is required and has a maximum length of 100 characters.
        description (str): A detailed description of the task. This field is optional.
        status_task (str): The current status of the task. This field is optional and defaults to "TO DO".
            Choices are:
                - "TO DO": The task is yet to be started.
                - "IN PROGRESS": The task is currently being worked on.
                - "DONE": The task has been completed.

    Meta:
        Inherits from BaseModel which includes:
        - id: A UUID field serving as the primary key.
        - date_created: A timestamp automatically set when the task is created.
        - last_updated: A timestamp automatically updated whenever the task is modified.

    """

    TASK_STATUS = (("TO DO", "TO DO"), ("IN PROGRESS", "IN PROGRESS"), ("DONE", "DONE"))

    user = models.ForeignKey(
        get_user_model(), related_name="users", on_delete=models.SET_NULL, null=True
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status_task = models.CharField(
        max_length=20, choices=TASK_STATUS, blank=True, default="TO DO"
    )

    def __str__(self):
        return self.title
