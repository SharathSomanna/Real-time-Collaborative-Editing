from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer, AsyncConsumer
import json
from channels.exceptions import StopConsumer
class MySyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        print("WebSocket connected...")
        #print("channel layer...", self.channel_layer)
        self.group_name = self.scope['url_route']['kwargs']['groupname']
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        from .models import Group, Document
        print("Message received from client...", event)
        self.group_name = self.scope['url_route']['kwargs']['groupname']
        data = json.loads(event['text'])
        group=Group.objects.get(name=self.group_name)
        doc=Document(
            content=data['msg'],
            group=group,
        )
        doc.save()
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type':'chat.message',
                'message':event['text']
            }
        )
    def chat_message(self, event):
        self.send({
            'type':'websocket.send',
            'text':event['message']
        })


    def websocket_disconnect(self, event):  # Correct metho d name
        print("WebSocket disconnected...")
        raise StopConsumer()


class MyAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("WebSocket connected...")
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print("Message received...")
        # You can send a message back to the client if needed
        await self.send({
            'type': 'websocket.send',
            'text': 'Hello from async server!'
        })

    async def websocket_disconnect(self, event):  # Correct method name
        print("WebSocket disconnected...")