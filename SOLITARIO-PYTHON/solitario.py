from random import random


class Card:

    # TODO change rank/suit to use ints, and create accessor methods that
    #      return the actual ranks/suits

    ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10',
             'Jack', 'Queen', 'King']
    suits = ['Hearts', 'Clubs', 'Diamonds', 'Spades']

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.name = self.rank + " of " + self.suit
        if self.suit == 'Hearts' or self.suit == 'Diamonds':
            self.tag = '+'
        else:
            self.tag = '-'
        self.tag += (self.rank[0] if self.rank != '10' else '0') + self.suit[0]

    def __str__(self):
        return self.name


class Deck:

    '''Creates an empty Deck object.'''
    def __init__(self):
        self.cards = []

    '''Populates the Deck with a standard 52-card arrangement.'''
    def populate(self):
        for rank in Card.ranks:
            for suit in Card.suits:
                self.cards.append(Card(rank, suit))

    '''Returns the size of the Deck.'''
    def size(self):
        return len(self.cards)

    '''Shuffles the deck using a single pass random selection algorithm.'''
    def shuffle(self):
        shuffledcards = []
        for i in range(0, self.size()):
            index = int(self.size() * random())
            shuffledcards.append(self.cards.pop(index))
        self.cards = shuffledcards

    '''Returns a number of Card objects from the Deck.'''
    def draw(self, count=1):
        cards = []
        if self.size() != 0:
            for i in range(0, count):
                cards.append(self.cards.pop())
            cards.reverse()
        return cards

    '''Returns a number of Card objects from a given location within the Deck.'''
    def draw_at(self, index, count=1):
        cards = []
        for i in range(0, count):
            cards.append(self.cards.pop(index))
        return cards

    '''Adds a list of Card objects to the Deck.'''
    def place(self, cards):
        self.cards.extend(cards)

    '''Returns a reference to the top card of the deck.'''
    def top_card(self):
        return self.cards[self.size()-1] if self.size() > 0 else None


class Solitaire:

    def __init__(self):
        self.deck = Deck()
        self.waste = Deck()
        self.foundation = [Deck() for i in range(0, 4)]
        self.facedown_tableau = [Deck() for i in range(0, 7)]
        self.faceup_tableau = [Deck() for i in range(0, 7)]
        self.deck.populate()

        self.deck.shuffle()
        for i in range(6, 0, -1):
            self.facedown_tableau[i].cards = self.deck.draw(i)
        for i in range(0, 7):
            self.faceup_tableau[i].cards = self.deck.draw()

    def display(self):
        output = '    W       E   R   T   Y\n'
        output += '%s %s     %s %s %s %s\n\n' % (
                ('XXX' if self.deck.size() > 0 else '   '),
                (self.waste.top_card().tag if self.waste.size() > 0 else '   '),
                (self.foundation[0].top_card().tag if self.foundation[0].size() > 0 else '   '),
                (self.foundation[1].top_card().tag if self.foundation[1].size() > 0 else '   '),
                (self.foundation[2].top_card().tag if self.foundation[2].size() > 0 else '   '),
                (self.foundation[3].top_card().tag if self.foundation[3].size() > 0 else '   '))
        output += '1   2   3   4   5   6   7\n'

        heights = [deck.size() for deck in self.facedown_tableau]
        for i, deck in enumerate(self.faceup_tableau):
            heights[i] += deck.size()

        for i in range(0, max(heights) + 1):
            for j in range(0, 7):
                fdheight = self.facedown_tableau[j].size()
                fuheight = self.faceup_tableau[j].size()
                if fdheight > i:
                    output += "XXX "
                else:
                    if fuheight + fdheight > i:
                        card = self.faceup_tableau[j].cards[i - fdheight]
                        output += card.tag + " "
                    else:
                        output += "    "
            output += "\n"

        print (output)

    def reveal(self):
        for i in range(0, 7):
            self.reveal_column(i)

    def reveal_column(self, column):
        if self.facedown_tableau[column].size() > 0:
            if self.faceup_tableau[column].size() == 0:
                self.faceup_tableau[column].place(self.facedown_tableau[column].draw())

    def draw(self):
        if self.deck.size() == 0:
            self.deck.place(self.waste.draw(self.waste.size()))
            self.deck.cards.reverse()
        self.waste.place(self.deck.draw())

    def move_card(self, from_deck, to_deck, foundation_move=False):
        if from_deck.size() > 0:
            if to_deck.size() == 0:
                if foundation_move:
                    if from_deck.top_card().rank == Card.ranks[0]:
                        to_deck.place(from_deck.draw())
                else:
                    if from_deck.top_card().rank == Card.ranks[12]:
                        to_deck.place(from_deck.draw())
            else:
                if self.is_placeable(from_deck.top_card(), to_deck.top_card(), foundation_move):
                    to_deck.place(from_deck.draw())

    def move_cards(self, from_deck, to_deck, count=None):
        if count is None:
            count = from_deck.size()
            if to_deck.size() == 0:
                if from_deck.cards[0].rank == Card.ranks[12]:
                    to_deck.place(from_deck.draw(count))
            else:
                for i, card in enumerate(from_deck.cards):
                    if self.is_placeable(card, to_deck.top_card()):
                        to_deck.place(from_deck.draw_at(i, count - i))
                        break
        else:
            if count > from_deck.size():
                count = from_deck.size()
            card = from_deck.cards[from_deck.size() - count]
            if to_deck.size() == 0:
                if card.rank == Card.ranks[12]:
                    i = from_deck.cards.index(card)
                    to_deck.place(from_deck.draw_at(i, count))
            else:
                if self.is_placeable(card, to_deck.top_card()):
                    i = from_deck.cards.index(card)
                    to_deck.place(from_deck.draw_at(i, count))

    def is_placeable(self, card, target_card, foundation_move=False):
        if foundation_move:
            if card.suit == target_card.suit and card.rank == Card.ranks[Card.ranks.index(target_card.rank)+1]:
                return True
            else:
                return False
        else:
            if (Card.suits.index(card.suit) % 2) + (Card.suits.index(target_card.suit) % 2) == 1 and card.rank == Card.ranks[Card.ranks.index(target_card.rank)-1]:
                return True
            else:
                return False

    def parse(self, command):
        command = command.upper().replace(' ', '')
        if len(command) == 0:
            return
        if command[0] == 'H':
            print('\nShorthand Commands:\nD = Draw a card from the deck\nE = Exit the game\nF = Fill foundation\nMxy = Move a single card from x to y (including foundation)\nN = New game\nR = Reveal applicable cards in the tableau (automatic by default\nSxyc = Shift c cards from x to y (excluding foundation; c is optional, i.e. Sxy works too)\n')
        elif command[0] == 'D':
            self.draw()
        elif command[0] == 'E':
            response = input('\nAre you sure you want to exit? (y/n): ')
            response = response.upper().replace(' ', '')
            if len(response) > 0 and response[0] == 'Y':
                self.exit()
        elif command[0] == 'F':
            self.fill_foundation()
        elif command[0] == 'M':
            if len(command) == 3:
                from_deck = self.get_deck(command[1])
                to_deck = self.get_deck(command[2])
                if from_deck is not None and to_deck is not None:
                    if command[2] in 'ERTY':
                        self.move_card(from_deck, to_deck, True)
                    elif command[2] in '1234567':
                        self.move_card(from_deck, to_deck, False)
        elif command[0] == 'N':
            response = input('\nAre you sure you want to start a new game? (y/n): ')
            response = response.upper().replace(' ', '')
            if len(response) > 0 and response[0] == 'Y':
                self.__init__()
        elif command[0] == 'R':
            self.reveal()
        elif command[0] == 'S':
            if len(command) >= 3:
                from_deck = self.get_deck(command[1])
                to_deck = self.get_deck(command[2])
                if from_deck is not None and to_deck is not None and command[1] in '1234567' and command[2] in '1234567':
                    self.move_cards(from_deck, to_deck)

    def get_deck(self, key):
        '''
            W = waste
            E/R/T/Y = Foundation 1-4
            1/2/3/4/5/6/7 = Tableau 1-7
        '''
        if key == 'W':
            return self.waste
        elif key in 'ERTY':
            return self.foundation['ERTY'.index(key)]
        elif key in '1234567':
            return self.faceup_tableau['1234567'.index(key)]
        else:
            return None

    def fill_foundation(self):
        # This method will move cards from the tableau to the foundation in
        # passes until a move hasn't occurred in a single pass over the tableau
        moved = True
        while moved:
            moved = False
            for i in range(0, 7):
                for j in range(0, 4):
                    if self.faceup_tableau[i].size() > 0:
                        if ((self.foundation[j].size() == 0 and
                             self.faceup_tableau[i].top_card().rank == Card.ranks[0]) or
                            (self.foundation[j].size() > 0 and
                             self.is_placeable(self.faceup_tableau[i].top_card(), self.foundation[j].top_card(), True))):
                            self.move_card(self.faceup_tableau[i], self.foundation[j], True)
                            moved = True

    ''' Game looping methods '''
    def start(self):
        self.playing = True
        while self.playing:
            self.play()

    def play(self):
        self.display()
        command = input('Enter a command (or \'help\'): ')
        self.parse(command)
        self.reveal()

    def exit(self):
        self.playing = False

if __name__ == '__main__':
    Solitaire().start()