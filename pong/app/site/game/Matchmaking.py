from .classPong import Pong

class Matchmaking():
    games = []

    def joinGame(self):
        nbGame = 0

        for game in self.games:
            if game.player2 == None:
                game.player2 = 'p2'
                return game
            nbGame += 1
        self.games.append(Pong('p1', nbGame))
        return self.games[nbGame]
    
    def endGame(self, game):
        if game.player1 == game.player2:
            game.player1.close()
        else:
            game.player1.close()
            game.player2.close()
        game.player2 = 'END'
        game.player1 = 'END'