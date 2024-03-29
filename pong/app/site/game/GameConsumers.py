import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .views import manager
from .views import managerTournament
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
        typeParty = text_data_json['typeParty']
        gameIdx = gameId - 1
        
        
        if gameIdx > len(manager.games):
            gameIdx = len(manager.games) - 1
        
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
            manager.games[gameIdx].scoreP1 = 0
            manager.games[gameIdx].scoreP1 = 0
        if game == 'tournamentInProgress':
            tournamentId = text_data_json['tournamentId']
            tournamentId = tournamentId - 1
            if manager.games[gameIdx].scoreP1 == 5:
                managerTournament.tournaments[tournamentId].winner = managerTournament.tournaments[tournamentId].match[0]
            elif manager.games[gameIdx].scoreP2 == 5:
                managerTournament.tournaments[tournamentId].winner = managerTournament.tournaments[tournamentId].match[1]
            managerTournament.tournaments[tournamentId].tournamentInProgress()
            managerTournament.tournaments[tournamentId].player1 = self
            managerTournament.tournaments[tournamentId].player2 = self
            if managerTournament.tournaments[tournamentId].match == None:
                managerTournament.tournaments[tournamentId].player1.send(text_data=json.dumps({
                    'type':'end',
                    'winner': managerTournament.tournaments[tournamentId].arrWinner[0]
                }))
                manager.endGame(manager.games[gameIdx])
                return
            managerTournament.tournaments[tournamentId].player1.send(text_data=json.dumps({
                'type':'players',
                'player1': managerTournament.tournaments[tournamentId].match[0],
                'player2': managerTournament.tournaments[tournamentId].match[1],
                'tournamentUsers': managerTournament.tournaments[tournamentId].arrWinner,
            }))
            manager.games[gameIdx].player1 = self
            manager.games[gameIdx].player2 = self
            manager.games[gameIdx].scoreP1 = 0
            manager.games[gameIdx].scoreP1 = 0

        if game == 'local':
            manager.games[gameIdx].player1 = self
            manager.games[gameIdx].player2 = self
        elif manager.games[gameIdx].player1 == 'p1':
            manager.games[gameIdx].player1 = self
        elif manager.games[gameIdx].player2 == 'p2':
            manager.games[gameIdx].player2 = self
        
        if type(manager.games[gameIdx].player1) != str and type(manager.games[gameIdx].player2) != str and manager.games[gameIdx].player2 != None and type(manager.games[gameIdx].player2) == type(manager.games[gameIdx].player1):
            try:
                manager.games[gameIdx].player1.send(text_data=json.dumps({
                    'type':'start',
                }))
                manager.games[gameIdx].player2.send(text_data=json.dumps({
                    'type':'start',
                }))
                manager.games[gameIdx].bar_moov(moov, self)
                manager.games[gameIdx].game(game, typeParty)
            except:
                pass
        else:
            print("Waiting room....")
    
    def disconnect(self, close_code):
        if close_code == 1001:
            for game in manager.games:
                if game.player1 == self or game.player2 == self:
                    try:
                        if type(game.player1) != str:
                            game.player1.close()

                        if type(game.player2) != str:
                            game.player2.close()
                    except:
                        pass
                    game.player2 = 'END'
                    game.player1 = 'END'
        raise StopConsumer

