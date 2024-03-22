import random
import threading

class Tournament:
    def __init__(self):
        self.users = None
        self.nb_user = None
        self.match = None
        self.have_played = None
        self.winner = None
        self.arrWinner = []

    def tournamentinit(self):
        player1 = random.randrange(0, self.nb_user)
        player2 = random.randrange(0, self.nb_user)
        while player1 == player2:
            player2 = random.randrange(0, self.nb_user)
        self.have_played = [self.users[player1], self.users[player2]]
        self.match = [self.users[player1], self.users[player2]]


    def tournamentInProgress(self):
        if self.winner != None:
            self.arrWinner.append(self.winner)

        if self.have_played != None:
            if len(self.have_played) == self.nb_user:
                if self.nb_user == 2 and len(self.have_played) == 2:
                    self.match = None
                    return
                self.nb_user = len(self.arrWinner)
                self.have_played.clear()
                self.users = self.arrWinner
                self.arrWinner = []
                self.have_played = None
                player1 = random.randrange(0, self.nb_user)
                player2 = random.randrange(0, self.nb_user)
                while player1 == player2:
                    player2 = random.randrange(0, self.nb_user)
                self.have_played = [self.users[player1], self.users[player2]]
            else:
                player1 = random.randrange(0, self.nb_user)
                if self.users[player1] not in self.have_played:
                    self.have_played.append(self.users[player1])
                else:
                    while self.users[player1] in self.have_played:
                        player1 = random.randrange(0, self.nb_user)
                    self.have_played.append(self.users[player1])
                
                player2 = random.randrange(0, self.nb_user)
                if self.users[player2] not in self.have_played:
                    self.have_played.append(self.users[player2])
                else:
                    while self.users[player2] in self.have_played:
                        player2 = random.randrange(0, self.nb_user)
                    self.have_played.append(self.users[player2])
        else:
            player1 = random.randrange(0, self.nb_user)
            player2 = random.randrange(0, self.nb_user)
            while player1 == player2:
                player2 = random.randrange(0, self.nb_user)
            self.have_played = [self.users[player1], self.users[player2]]
        self.match = [self.users[player1], self.users[player2]]