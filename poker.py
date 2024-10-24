SUITS = ['h', 'd', 'c', 's']
NUMS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


class Card:
    def __init__(self, num, suit):
        self.num = num
        self.suit = suit
    def __repr__(self):
        return f'{NUMS[self.num]}{self.suit}'

class Range:
    def __init__(self, range):
        self.range = range
    def __iter__(self):
        self._iter = iter(self.range)
        return self._iter
    def __next__(self):
        return self._iter.__next__()

class Hand:
    def __init__(self, cards):
        self.hand_class = 0

        self.cards = sorted(cards, key=lambda x: x.num, reverse=True)


        # straights, flushes, straight flushes
        self.straights = self.__straight__(cards)
        self.flushes = self.__flush__(cards)
        self.straight_flush = self.__straight__(cards, straight_flush=True)

        # pairs, trips, quads
        self.matches = [[] for _ in range(len(NUMS))]
        for card in cards:
            self.matches[card.num] += [card]
        self.matches.reverse()

        self.pairs = []
        self.trips = []
        self.quads = []

        for match in self.matches:
            length = len(match)
            if length == 2:
                self.pairs += [match]
            elif length == 3:
                self.trips += [match]
            elif length == 4:
                self.quads += [match]

        # two pair
        if len(self.pairs) > 1:
            self.pair2 = self.pairs[:2]
        else:
            self.pair2 = []

        # boats / full house
        if len(self.pairs) > 0 and len(self.trips) > 0:
            self.boats = (self.trips[0], self.pairs[0])
        else:
            self.boats = ()

        # calculate hand class
        if self.straight_flush:
            self.hand_class = 8
            self.best_hand = self.straight_flush
        elif self.quads:
            self.hand_class = 7
            self.best_hand = self.quads[0]
        elif self.boats:
            self.hand_class = 6
            self.best_hand = self.boats
        elif self.flushes:
            self.hand_class = 5
            self.best_hand = self.flushes
        elif self.straights:
            self.hand_class = 4
            self.best_hand = self.straight_flush
        elif self.trips:
            self.hand_class = 3
            self.best_hand = self.trips[0] + [card for card in self.cards if card not in self.trips[0]][:3]
        elif self.pair2:
            self.hand_class = 2
            self.best_hand = self.pairs[0] + self.pairs[1] + [card for card in self.cards if card not in self.pair2[0]][:1]
        elif self.pairs:
            self.hand_class = 1
            self.best_hand = self.pairs[0] + [card for card in self.cards if card not in self.pairs[0]][:4]
        else:
            self.hand_class = 0
            self.best_hand = self.cards[:5]





    def __straight__(self, cards, straight_flush=False):
        # sort by suit as well if straight_flush
        if straight_flush:
            cards = sorted(cards, key=lambda x: x.num + 100*SUITS.index(x.suit), reverse=True)

        counter = 4
        straight = [cards[0]]
        for i in range(1, len(cards)):
            if cards[i].num == cards[i-1].num:
                continue
            elif cards[i].num + 1 == cards[i-1].num:
                straight += [cards[i]]
            else:
                straight = [cards[i]]
                counter = 4
            
            if len(straight) == 5:
                return straight


        return []

    def __flush__(self, cards):
        flushes = {suit : [] for suit in SUITS}
        for card in cards:
            flushes[card.suit] += [card]
            if len(flushes[card.suit]) == 5:
                return flushes[card.suit]

        return []
            

    def __repr__(self):
        return ' '.join([str(card) for card in self.cards])

    def __eq__(hero, vill):
        return hero.best_hand == vill.best_hand

    def __gt__(hero, vill):
        if hero.hand_class == vill.hand_class:
            for h, v in zip(hero.best_hand, vill.best_hand):
                if h.num != v.num:
                    return h.num > v.num
            return False
        
        else:
            return hero.hand_class > vill.hand_class
    
    def __lt__(hero, vill):
        if hero.hand_class == vill.hand_class:
            for h, v in zip(hero.best_hand, vill.best_hand):
                if h.num != v.num:
                    return h.num < v.num
            return False
        
        else:
            return hero.hand_class < vill.hand_class

    def __le__(hero, vill):
        return hero == vill or hero < vill
    
    def __ge__(hero, vill):
        return hero == vill or hero > vill



class Game:
    deck = {f'{NUMS[num]}{suit}' : Card(num, suit) for suit in SUITS for num in range(13)}

    players = []



hero = Hand([
    deck['Qh'],
    deck['Jh'],
    deck['10h'],
    deck['10d'],
    deck['9h'],
    deck['9c']
    ])

vill = Hand([
    deck['Qh'],
    deck['Qc'],
    deck['Qd'],
    deck['Qs'],
    deck['Ah'],
    ])
    