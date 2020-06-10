# Блек-джек
# Від 1 до 7 гравців проти дилера

import cards
import games


class BJ_Card(cards.Card):
    """Card for game Black Jack"""
    ACE_VALUE = 1

    @property
    def value(self):
        if self.face_up:
            v = BJ_Card.RANKS.index(self.rank) + 1
            if v > 10:
                v = 10
        else:
            v = None
        return v


class BJ_Deck(cards.Deck):
    """Deck for a play in 'Black Jack'"""

    def populate(self):
        for suit in BJ_Card.SUITS:
            for rank in BJ_Card.RANKS:
                self.cards.append(BJ_Card(rank, suit))


class BJ_Hand(cards.Hand):
    """'Hand': set cards 'Black Jack' in a one player."""

    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        rep = self.name + ':\t' + super().__str__()
        if self.total:
            rep += '(' + str(self.total) + ')'
        return rep

    @property
    def total(self):
        for card in self.cards:
            if not card.value:
                return None

        t = 0
        for card in self.cards:
            t += card.value

        contains_ace = False
        for card in self.cards:
            if card.value == BJ_Card.ACE_VALUE:
                contains_ace = True

        if contains_ace and t <= 11:
            t += 10
        return t

    def is_busted(self):
        return self.total > 21


class BJ_Player(BJ_Hand):
    """Black Jack Player"""

    def is_hitting(self):
        response = games.ask_yes_no('\n' + self.name + '. Будете брати ще карти? (Y/N): ')
        return response == 'y'

    def bust(self):
        print(self.name, ' перебрав.')
        self.lose()

    def lose(self):
        print(self.name, ' програв.')

    def win(self):
        print(self.name, ' переміг.')

    def push(self):
        print(self.name, ' зіграв з комп*ютером в нічию.')


class BJ_Dealer(BJ_Hand):
    """Dealer in a game 'Black Jack'"""

    def is_hitting(self):
        return self.total < 17

    def bust(self):
        print(self.name, ' перебрав.')

    def flip_first_card(self):
        first_card = self.cards[0]
        first_card.flip()


class BJ_Game:
    """Game in Black Jack"""

    def __init__(self, names):
        self.players = []
        for name in names:
            player = BJ_Player(name)
            self.players.append(player)
        self.dealer = BJ_Dealer('Dealer')
        self.deck = BJ_Deck()
        self.deck.populate()
        self.deck.shuffle()

    @property
    def still_playing(self):
        """Return list of players in the Game"""
        sp = []
        for player in self.players:
            if not player.is_busted():
                sp.append(player)
        return sp

    def __additional_cards(self, player):
        while not player.is_busted() and player.is_hitting():
            self.deck.deal([player])
            print(player)
            if player.is_busted():
                player.bust()

    def play(self):
        # Give all 2 cards
        self.deck.deal(self.players + [self.dealer], per_hand=2)
        self.dealer.flip_first_card()  # flip first dealer card
        for player in self.players:
            print(player)
        print(self.dealer)
        #  delivery of additional cards
        for player in self.players:
            self.__additional_cards(player)
        self.dealer.flip_first_card()  # dealer's first card is revealed
        if not self.still_playing:
            print(self.dealer)
        else:
            # give  dealer the additional cards
            print(self.dealer)
            self.__additional_cards(self.dealer)
            if self.dealer.is_busted():
                # Everyone who stays in the game wins
                for player in self.still_playing:
                    player.win()
            else:
                # compare the sums of points from the dealer and the players
                for player in self.still_playing:
                    if player.total > self.dealer.total:
                        player.win()
                    elif player.total < self.dealer.total:
                        player.lose()
                    else:
                        player.push()
        # delete all cards
        for player in self.players:
            player.clear()
        self.dealer.clear()


def main():
    print('\t\tЛаскаво просимов за ігровий стіл Блек Джека!\n')
    names = []
    number = games.ask_number('Скільки всього гравців? (1-7): ', low=1, high=8)
    for i in range(number):
        name = input("Введіть ім'я гравця: ")
        names.append(name)
        print()
    game = BJ_Game(names)
    again = None
    while again != 'n':
        game.play()
        again = games.ask_yes_no('Бажаєте зіграти ще? (y/n): ')
        main()
    input('\n\nНатисніть Enter щоб вийти.')


if __name__ == '__main__':
    main()
