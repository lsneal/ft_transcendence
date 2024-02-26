from .Tournament import Tournament

class MatchmakingTournament():    
    tournaments = []

    def joinTournament(self):
        self.tournaments.append(Tournament())