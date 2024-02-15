import random
from time import sleep

from flask import current_app

from app.models.player import Player
from app.utils import generate_random_string


class GameStatus:
    # init = 'init'
    waiting = 'waiting'
    starting = 'starting'
    started = 'started'
    ended = 'ended'


class Game:

    def __init__(self, n_players: int) -> None:
        self.players: list[Player] = []
        self.game_id = random.randint(0, 10)
        self.n_players = n_players

        self.status = GameStatus.waiting

        current_app.games.append(self)

        pass

    def set_status(self, status: str):
        self.status = status

    def add_player_to_game(self, username: str, http_session):

        uid = generate_random_string(5)

        player = Player(username=username, uid=uid, http_session=http_session, game_id=self.game_id)
        self.players.append(player)

        http_session['game_id'] = self.game_id
        http_session['username'] = username
        http_session['uid'] = uid

        # TODO fare controlli

        pass

    def remove_player(self):
        pass

    def get_player_by_name(self, username: str) -> Player:
        for p in self.players:
            if p.username == username:
                return p

    @staticmethod
    def get_game_by_id(id: int) -> 'Game':
        for game in current_app.games:
            if game.game_id == id:
                return game

    def check_game_starting(self):
        if len(self.players) == self.n_players:
            #     il gioco può iniziare
            self.status = GameStatus.starting
            #     devo avvisare i players che il gioco può avviarsi

            for p in self.players:
                p.send_event('game_starting', {'msg': 'La partita sta per iniziare'})
            # emit('game_starting', {'msg': 'La partita sta per iniziare'})

            sleep(10)

            self.start_game()

    def start_game(self):
        self.status = GameStatus.started
        # self.send_broadcast_msg('start_game', {})

    #     3 round piccoli
    #     1 round grande
    #     1 round di stoppa

    def send_broadcast_msg(self, event, args):
        for p in self.players:
            p.send_event(event, args)

    def __str__(self) -> str:
        return f'Room n. {self.code}; Players: {len(self.players)}'

    def __repr__(self) -> str:
        return self.__str__()
