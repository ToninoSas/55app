from app.models.card import Card, Types


class Shuffle:
    def __init__(self):
        self.cards = []
        self.__gen_mazzo()

        # mischio per tre volte
        for _ in range(0, 3):
            self.__shuffle()

        # self.__print()

    def __gen_mazzo(self):
        for i in range(1, 11):
            card = Card(i, Types.bastoni)
            self.cards.append(card)

        for i in range(1, 11):
            card = Card(i, Types.spade)
            self.cards.append(card)

        for i in range(1, 11):
            card = Card(i, Types.coppe)
            self.cards.append(card)

        for i in range(1, 11):
            card = Card(i, Types.denari)
            self.cards.append(card)

    def __shuffle(self):
        import random
        # mischiare il mazzo
        n = len(self.cards)
        for i in range(0, n - 2):
            j = random.randint(i, n - 1)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

    def __print(self):
        for card in self.cards:
            print(card)
