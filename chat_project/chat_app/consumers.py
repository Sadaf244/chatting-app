import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import *
# def store(request):
#     connection_id = request.GET.get('connection')
#     print(connection_id)
#     return True
# def store(self, request):  
#         message = self.message
#         user1 = request.GET.get('user1')
#         user2 = request.GET.get('user2')
#         connection_id = request.GET.get('connection')
#         print('ssdsd')
#         # Now you can save the message to the Message model using the connection_id and other relevant information
#         # For example:
#         connection = Connection.objects.get(id=connection_id)
#         sender = ChatUser.objects.get(username=user1)
#         receiver = ChatUser.objects.get(username=user2)
#         new_message = Message.objects.create(connection=connection, sender=sender, receiver=receiver, content=message)
#         new_message.save()
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
   

    def receive(self, text_data):
        connection=Connection.objects.order_by('-id')[0]
        sender=ChatUser.objects.get(id=connection.user1.id)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        Message.objects.create(content=message,sender=sender,connection=connection).save()
       
        print(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message
            }
        )

    def chat_message(self, event):
        message = event['message']
        print(event)
        # store(request)
        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message
        }))
    #     self.store(message)
    