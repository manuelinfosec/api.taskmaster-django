from typing import Optional

from channels.layers import get_channel_layer


async def send_task(group_name: str, data: Optional[dict] = None) -> None:
    """
    Task Stream

    required parameters:

    group_name: group name to send message to.

    Optional parameters:

    data: a dictionary containing task details.
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
