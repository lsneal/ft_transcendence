import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .views import manager
from django.contrib.auth.models import AnonymousUser

class GameConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['game_name']
        self.room_group_name = 'game_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        moov = text_data_json['moov']
        game = text_data_json['game']
        gameId = text_data_json['gameId']

        if manager.games[gameId].player1 == 'p1':
            manager.games[gameId].player1 = self
        elif manager.games[gameId].player2 == 'p2':
            manager.games[gameId].player2 = self

        if manager.games[gameId].player1 != 'p1' and manager.games[gameId].player2 != 'p2' and manager.games[gameId].player2 != None:
            manager.games[gameId].bar_moov(moov)
            manager.games[gameId].game(game)
        else:
            print("Waiting room....")


#chat ->
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