'''CAH game logic'''

CAH_PLAYERS = {}

CAH_STARTED = False
CAH_ENDED = False

CAH_NSFW = False
CAH_B_DECK = set()
CAH_B_DECK_NSFW = set()
CAH_W_DECK = set()
CAH_W_DECK_NSFW = set()

CAH_TSAR = None
CAH_NUM = 5
CAH_TURNED_CARDS = {}


'''Player class storing info'''
class CAH_Player:
    def __init__(self,name, hand: list, id):
        self.name = name
        self.hand = hand
        self.score = 0
        self.turn = False
        self.id = id
        
    '''---------
    - dm the cards? (UI problem)
    - once all cards are turned in, reveal all without the names and let the tsar choose by number
    (keep the turned in cards with a dictionary? name as key and card as value)
    -----------'''
            
def add_player(name, id):
    global CAH
    CAH_PLAYERS[name] = CAH_Player(name, _random_cards(CAH_NUM), id)
    
    
    
'''hand is a list of 2-tuples with first value being number and second the text'''
def _random_cards(num) -> list:
    global CAH_W_DECK
    hand = []
    card_count = 1
    for i in range(num):
        card = CAH_W_DECK.pop()
        hand.append((card_count, card),)  
        card_count += 1 
    return hand
