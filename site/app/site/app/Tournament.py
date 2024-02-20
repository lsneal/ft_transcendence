import random
import threading

class Tournament:

    def __init__(self):
        self.users = None
        self.nb_user = None
        self.current_round = None
        self.match = None
        self.matchId = None
        self.max_round = None
        self.have_played = None
        self.winner = None
        self.arrWinner = []

    def tournamentinit(self):
        if self.winner != None:
            self.arrWinner.append(self.winner)


        if self.have_played != None and len(self.have_played) != 0:
            self.current_round = len(self.have_played) / 2
        else:
            self.current_round = 0
        self.max_round = self.nb_user - 2
        
        if self.have_played != None:
            if len(self.have_played) == self.nb_user:
                self.have_played.clear()
                self.nb_user = len(self.arrWinner)
                if self.nb_user == 1:
                    self.match = None
                    return
                self.users = self.arrWinner
                self.arrWinner = []
                self.have_played = None
                player1 = random.randrange(0, self.nb_user)
                player2 = random.randrange(0, self.nb_user)
                while player1 == player2:
                    player2 = random.randrange(0, self.nb_user)
                self.have_played = [player1, player2]
            else:

                for player in self.have_played:
                    player1 = random.randrange(0, self.nb_user)
                    if player != player1:
                        self.have_played.append(player1) 
                        break

                for player in self.have_played:
                    player2 = random.randrange(0, self.nb_user)
                    if player != player2 and player2 != player1:
                        self.have_played.append(player2)
                        break
        else:
            player1 = random.randrange(0, self.nb_user)
            player2 = random.randrange(0, self.nb_user)
            while player1 == player2:
                player2 = random.randrange(0, self.nb_user)
            self.have_played = [player1, player2]
        self.match = [self.users[player1], self.users[player2]]
        self.matchId = [player1, player2]

