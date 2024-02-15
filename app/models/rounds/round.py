from app.models.player import Player


class Round:
    def __init__(self, players: list[Player], montepremi: int) -> None:
        self.players = players
        self.montepremi = montepremi



