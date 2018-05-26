'''CAH game logic'''


'''Game class storing info'''
class CAH_game:
    def __init__(self):
        self.CAH_PLAYERS = {}
        self.CAH_STARTED = False
        self.CAH_ENDED = False

        self.CAH_NSFW = False
        self.CAH_B_DECK = set()
        self.CAH_B_DECK_NSFW = set()
        self.CAH_W_DECK = set()
        self.CAH_W_DECK_NSFW = set()

        self.CAH_TSAR = None
        self.CAH_NUM = 5
        self.CAH_TURNED_CARDS = {}
        self.CAH_SCORE = 7
        
    '''Add a new player'''
        
    def add_player(self, name, id):
        self.CAH_PLAYERS[name] = CAH_Player(name, self._random_cards(self.CAH_NUM), id)
        
    '''Set up the game'''
        
    def set_up(self):
        self.CAH_STARTED = True
        if self.CAH_NSFW == True:
            self.CAH_W_DECK = self.CAH_W_DECK + self.CAH_W_DECK_NSFW
            self.CAH_B_DECK = self.CAH_B_DECK + self.CAH_B_DECK_NSFW
        for player in self.CAH_PLAYERS:
            self.CAH_PLAYERS[player].hand = self.random_cards(self.CAH_NUM)
            
    def _random_cards(self, num) -> list:
        hand = []
        card_count = 1
        for i in range(num):
            card = self.CAH_W_DECK.pop()
            hand.append((card_count, card),)  
            card_count += 1 
        return hand
    
'''Player class storing info'''
class CAH_Player:
    def __init__(self,name, hand: list, id):
        self.name = name
        self.hand = hand
        self.score = 0
        self.turn = False
        self.id = id
        

    
    
    


