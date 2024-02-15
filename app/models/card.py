class Types:
    bastoni = 'bastoni'
    spade = 'spade'
    coppe = 'coppe'
    denari = 'denari'


class Card:
    __scores = {
        1: 16,
        2: 12,
        3: 13,
        4: 14,
        5: 15,
        6: 18,
        7: 21,
        8: 10,
        9: 10,
        10: 10
    }

    def __init__(self, number: int, type: str) -> None:
        self.number = number
        self.type = type

        self.score = self.__scores[self.number]

    def __str__(self) -> str:
        return f"{self.number} di {self.type}."

    def __repr__(self) -> str:
        return str(self)
