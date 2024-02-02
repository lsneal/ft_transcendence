from .classPong import Pong

class Matchmaking():
    games = []
    
    def joinGame(self, user):
        pos = 0

        for game in self.games:
            if game.player2 == None:
                game.player2 = 'p2'
                return game.id
            pos += 1
        self.games.append(Pong('p1', pos))
        return pos

        


