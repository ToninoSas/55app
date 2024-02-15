import random
from flask import Flask, render_template, request, current_app, session, redirect, url_for
from app.extensions import socketio
from app.models.game import Game
from app.socket.events import init_socket_events

from app.utils import generate_random_string

app = Flask(__name__)
socketio.init_app(app)

app.secret_key = 'kitemmurt'

with app.app_context():
    current_app.games = []

# import blueprints

# listen events
init_socket_events(socketio)

@app.get('/')
def home_screen():
    return '<h1>Home!</h1>'

@app.get('/game')
def game_screen():

    username = session.get('username')
    game_id = session.get('game_id')
    uid = session.get('uid')

    if not username or not game_id or not uid:
        return redirect(url_for('join_screen'))

    return render_template('game.html', data={"username": username, "game_id": game_id, "uid": uid})


@app.route('/create', methods=["POST", "GET"])
def create_screen():
    if request.method == "GET":
        return render_template('create.html')
    elif request.method == "POST":
        username = request.values.get('username')
        n_players = int(request.values.get('n_players'))

        game = Game(n_players=n_players)
        game.add_player_to_game(username=username, http_session=session)

        return redirect(url_for('game_screen'))


@app.route('/join', methods=["POST", "GET"])
def join_screen():
    if request.method == "GET":
        return render_template('join.html')
    elif request.method == "POST":
        username = request.values.get('username')
        game_id = int(request.values.get('game_id'))

        game = Game.get_game_by_id(game_id)

        if not game:
            return redirect(url_for('home_screen'))

        game.add_player_to_game(username=username, http_session=session)

        return redirect(url_for('game_screen'))

if __name__ == '__main__':
    socketio.run(app)
