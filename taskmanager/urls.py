"""Task Manager URLs"""

from django.urls import path

from taskmanager.consumers import AsyncTaskNotificationConsumer
from taskmanager.views import CreateTaskAPI, ListTasksAPI, RetrieveUpdateDeleteTaskAPI

urlpatterns = [
    path("tasks/", ListTasksAPI.as_view(), name="list_tasks"),
    path("tasks/create/", CreateTaskAPI.as_view(), name="create_task"),
    path(
        "tasks/<uuid:task_id>/",
        RetrieveUpdateDeleteTaskAPI.as_view(),
        name="retrieve_update_delete_task",
    ),
]


ws_urlpatterns = [
    path(
        "ws/tasks/",
        AsyncTaskNotificationConsumer.as_asgi(),
        name="ws_task_notification",
    ),
]
