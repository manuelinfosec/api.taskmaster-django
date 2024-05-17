import time
import json
import uuid

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from accounts.models import User as UserModel
from taskmanager.models import Task as TaskModel
from taskmaster.utils import get_object_or_error


class AsyncTaskNotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.group_name = "task_stream"
        self.user: UserModel = self.scope.get("user")
        self.task_id = self.scope["url_route"]["kwargs"]["id"]

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):

        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_task(self, event: dict):
        message = event["message"]
        await self.send_json(content=message)
