import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .views import manager
from .views import managerTournament
from django.contrib.auth.models import AnonymousUser
from channels.exceptions import StopConsumer

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

        if game == 'tournament':
            tournamentId = text_data_json['tournamentId']
            tournamentId = tournamentId - 1
            users = text_data_json['users']
            nb_user = text_data_json['nb_user']
            managerTournament.tournaments[tournamentId].users = users
            managerTournament.tournaments[tournamentId].nb_user = nb_user
            managerTournament.tournaments[tournamentId].tournamentinit()
            managerTournament.tournaments[tournamentId].player1 = self
            managerTournament.tournaments[tournamentId].player2 = self
            managerTournament.tournaments[tournamentId].player1.send(text_data=json.dumps({
                'type':'players',
                'player1': managerTournament.tournaments[tournamentId].match[0],
                'player2': managerTournament.tournaments[tournamentId].match[1],
            }))
            manager.games[gameIdx].player1 = self
            manager.games[gameIdx].player2 = self
        if game == 'local':
            manager.games[gameIdx].player1 = self
            manager.games[gameIdx].player2 = self
        elif manager.games[gameIdx].player1 == 'p1':
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
    
    def disconnect(self, close_code):
        if close_code == 1001:
             
            for game in manager.games:
                if game.player1 == self or game.player2 == self:
                    game.player1.close()
                    game.player2.close()
        raise StopConsumer

