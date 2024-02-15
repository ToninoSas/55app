# socket_events.py
from flask import session
from flask_socketio import SocketIO, emit

from app.models.game import Game, GameStatus


def init_socket_events(socketio: SocketIO):
    @socketio.on('check_client_data')
    def on_check_data(data: dict):
        username = data.get('username')
        uid = data.get('uid')
        game_id = data.get('game_id')

        game = Game.get_game_by_id(game_id)

        if not game:
            emit('error', {'error': 'game not found'})
            return

        player = game.get_player_by_name(username)

        if not player:
            emit('error', {'error': 'player not found in game'})
            return

        if player.uid != uid:
            emit('error', {'error': 'uid given dosn\'t match with username'})
            return

        player.set_socket(socketio=socketio)
        socketio.emit('login_success')

        # IL PLAYER ORA è ENTRATO EFFETTIVAMENTE E I SUOI DATI SONO VALIDI
        # POSSO INIZIARE A VEDERE SE LA PARTITA PUò ESSERE AVVIATA
        # if game.status != GameStatus.started:
        #     game.check_game_starting()

        game.start_game()

    @socketio.on('game_info')
    def on_game_info():

        game_id = session['game_id']
        username = session['username']

        game = Game.get_game_by_id(game_id)

        if not game:
            emit('error', {'error': 'game not found'})
            return

        game_data = {
            'max_players': game.n_players,
            'n_players_now': len(game.players),
            'players': [p.username for p in game.players],
            'status': game.status,
            'game_id': game.game_id
        }

        if game.status == GameStatus.started:
            print('il gioco è in esecuzione')
        #     emit setup table
        #     emit('show_game_table', game_data)
        #     pass
            return game_data
        else:
            return game_data
