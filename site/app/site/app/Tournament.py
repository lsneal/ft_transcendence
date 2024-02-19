import random

class Tournament:

    def __init__(self):
        self.users = None
        self.nb_user = None
        self.current_round = None
        self.match = None
        self.max_round = None
        self.have_played = None

    def tournamentinit(self):
        if self.have_played != None or 0:
            self.current_round = self.have_played / 2
        else:
            self.current_round = 0

        self.max_round = self.nb_user - 2
        player1 = random.randrange(0, self.nb_user)
        player2 = random.randrange(0, self.nb_user)
        while player2 == random.randrange(0, self.nb_user):
            player2 = random.randrange(0, self.nb_user)
        
        self.match = [self.users[player1], self.users[player2]]
        self.have_played = [player1, player2]