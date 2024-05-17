from channels.generic.websocket import AsyncJsonWebsocketConsumer


class AsyncTaskNotificationConsumer(AsyncJsonWebsocketConsumer):
    """
    WebSocket consumer to handle task notifications asynchronously.
    """

    async def connect(self):
        """
        Handles the WebSocket connection event.
        Adds the current WebSocket connection to a group and accepts the connection.
        """
        # Define a group name for WebSocket communication
        self.group_name = "task_stream"

        # Add the current channel to the group
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, code):
        """
        Handles the WebSocket disconnection event.
        Removes the current WebSocket connection from the group.

        Args:
            code (int): The disconnection code.
        """
        # Remove the current channel from the group when the WebSocket connection is closed
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_task(self, event: dict):
        """
        Sends a task notification message to the WebSocket client.

        Args:
            event (dict): The event dictionary containing the message to be sent.
        """
        # Retrieve the message from the event dictionary
        message = event["message"]

        # Send the message to the WebSocket client as JSON
        await self.send_json(content=message)
