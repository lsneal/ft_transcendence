from .classPong import Pong

class Matchmaking():
    games = []
    
    def joinGame(self, id):
        pos = id
        print("result ======================", pos)
        for game in self.games:
            if self.games[pos].player2 == None:
                self.games[pos].player2 = 'p2'
                return self.games[pos]
        self.games.append(Pong('p1', pos))
        return self.games[pos]


    def endGame(self, gameId):
        for game in self.games:
            if game.id == gameId:
                self.games.remove(game)
                return
