from .classPong import Pong

class Matchmaking():
    games = []

    def joinGame(self):
        nbGame = 0

        for game in self.games:
            if game.player2 == None and game.player1_name == 'p1':
                game.player2 = 'p2'
                return game
            nbGame += 1
        self.games.append(Pong('p1', nbGame, 'p1'))
        return self.games[nbGame]
    
    def joinGameOnline(self, player):
        nbGame = 0

        for game in self.games:
            if game.player2 == None:
                game.player2 = 'p2'
                game.player2_name = player
                return game
            nbGame += 1
        self.games.append(Pong('p1', nbGame, player))
        return self.games[nbGame]

    def endGame(self, game):
        try:
            if game.player1 == game.player2 and game.player1  != 'END':
                game.player1.close()
            elif game.player1  != 'END' and game.player2 != 'END':
                game.player1.close()
                game.player2.close()
            game.player2 = 'END'
            game.player1 = 'END'
        except:
            pass