import json

from channels.generic.websocket import AsyncWebsocketConsumer


class StatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # Add the user to the status personal group
        self.personal_group_name = "status_single_test"
        if self.channel_layer:
            await self.channel_layer.group_add(
                self.personal_group_name, self.channel_name
            )

    async def disconnect(self, code):
        # Remove the user from the status personal group
        if self.channel_layer:
            await self.channel_layer.group_discard(
                self.personal_group_name, self.channel_name
            )

    # Handle "status" type
    async def status(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": event["type"],
                    "code": event["code"],
                    "message": event["message"],
                }
            )
        )
