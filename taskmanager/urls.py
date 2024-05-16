"""Task Manager URLs"""

from django.urls import path
from taskmanager.views import CreateTaskAPI, RetrieveUpdateDeleteTaskAPI, ListTasksAPI

urlpatterns = [
    path("tasks/", ListTasksAPI.as_view(), name="list_tasks"),
    path("tasks/create/", CreateTaskAPI.as_view(), name="create_task"),
    path(
        "tasks/<uuid:task_id>/",
        RetrieveUpdateDeleteTaskAPI.as_view(),
        name="retrieve_update_delete_task",
    ),
]
