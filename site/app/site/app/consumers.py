import json
import sys
import time 
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        moov = text_data_json['moov']
                           
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'game_moov',
                'moov':moov
            }
        )
    i = 0
    def game_moov(self, event):
        moov = event['moov']

        self.send(text_data=json.dumps({
            'type':'game',
            'moov':moov
        }))
        if i < 100:
            print("sleep: ", moov,file=sys.stderr)
            time.sleep(1)

#    def receive(self, text_data):
#        text_data_json = json.loads(text_data)
#        message = text_data_json['message']
#
#        async_to_sync(self.channel_layer.group_send)(
#            self.room_group_name,
#            {
#                'type':'chat_message',
#                'message':message
#            }
#        )
#    
#    def chat_message(self, event):
#        message = event['message']
#
#        self.send(text_data=json.dumps({
#            'type':'chat',
#            'message':message
#        }))