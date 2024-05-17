from typing import Optional

from channels.layers import get_channel_layer


async def send_task(group_name: str, data: Optional[dict] = None) -> None:
    """
    Send Task Notification

    This function is called from within the Task Create Service and is responsible for sending task notifications
    to a specified group via WebSocket. It calls the `send_task` method within the `AsyncTaskNotificationConsumer`.

    Required parameters:
    group_name: str - The name of the group to send the message to.

    Optional parameters:
    data: dict (optional) - A dictionary containing task details.
    """
    channel_layer = get_channel_layer()

    if not channel_layer:
        return None
    
    print(data)

    await channel_layer.group_send(
        group_name,
        {
            "type": "send_task",
            "message": data,
        },
    )
