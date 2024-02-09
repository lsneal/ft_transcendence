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
        gameIdx = gameId - 1


        if manager.games[gameIdx].player1 == 'p1':
            manager.games[gameIdx].player1 = self
        elif manager.games[gameIdx].player2 == 'p2':
            manager.games[gameIdx].player2 = self

        if manager.games[gameIdx].player1 != 'p1' and manager.games[gameIdx].player2 != 'p2' and manager.games[gameIdx].player2 != None:
            manager.games[gameIdx].player1.send(text_data=json.dumps({
                'type':'start',
            }))
            manager.games[gameIdx].player2.send(text_data=json.dumps({
                'type':'start',
            }))
            manager.games[gameIdx].bar_moov(moov, self)
            manager.games[gameIdx].game(game)
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