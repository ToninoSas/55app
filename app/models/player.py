from flask_socketio import SocketIO

from app.models.card import Types, Card


class Player:

    def __init__(self, username: str, uid: str, game_id, http_session) -> None:
        self.username = username
        self.uid = uid
        self.game_id = game_id
        self.http_session = http_session

        # LOGIC VARIABLES
        # le carte che il player avrà in mano ogni turno
        self.hand = []
        # le carte che il player avrà in mano al punto grande e alla stoppa
        self.final_hand = []
        # lo score che il player avrà ogni turno
        self.turn_score = 0
        self.bet = 0
        self.denaro = 100

    def set_socket(self, socketio: SocketIO):
        self.socketio = socketio

    def send_event(self, event: str, args: str):
        self.socketio.emit(event, args)

    def __calcola_score(self, cards: list[Card]) -> int:
        score = 0

        # devo prendere tutti i pali delle carte che ho in mano
        types = [card.type for card in cards]

        # prendo i pali delle carte della mano
        unique_types = set(types)

        # tutti tipi diversi
        if len(cards) == len(unique_types):
            score = max([card.score for card in cards])
            return score

        bastoni_cards = sorted([
            card for card in cards if card.type == Types.bastoni], key=lambda x: x.score, reverse=True)[0:3]
        coppe_cards = sorted([
            card for card in cards if card.type == Types.coppe], key=lambda x: x.score, reverse=True)[0:3]
        denari_cards = sorted([
            card for card in cards if card.type == Types.denari], key=lambda x: x.score, reverse=True)[0:3]
        spade_cards = sorted([
            card for card in cards if card.type == Types.spade], key=lambda x: x.score, reverse=True)[0:3]

        scores = {
            sum([card.score for card in bastoni_cards]): bastoni_cards,
            sum([card.score for card in coppe_cards]): coppe_cards,
            sum([card.score for card in denari_cards]): denari_cards,
            sum([card.score for card in spade_cards]): spade_cards
        }

        # prendo le carte che hanno il max punteggio
        max_score = max(scores)
        max_score_cards = scores.get(max_score)

        print(f'Max score cards: {max_score_cards}')

        return max_score

    def show_score(self, is_final: bool = False):
        if is_final:
            self.turn_score = self.__calcola_score(cards=self.final_hand)
        else:
            self.turn_score = self.__calcola_score(cards=self.hand)

        # CAPIRE SE MOSTRARE TUTTO IL PUNTEGGIO O MENO
        # far scegliere al giocatore quale carta togliere dal conteggio dei punti
        # print(self.turn_score)

        self.socketio.emit('show_player_score', {
            'username': self.username,
            'score': self.turn_score
        })

    def reset(self):
        self.hand.clear()
        self.bet = 0
        self.turn_score = 0

    def __str__(self) -> str:
        return f"{self.username}"

    def __repr__(self) -> str:
        return str(self)
