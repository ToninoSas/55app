var json_raw = $('#game_data').text()
var game_data = JSON.parse(json_raw)
console.log('dati ricevuti dalla sessione:' + json_raw)

var error_tag = $('#error_tag')
var nPlayersNowTag = $('#n_players_now')
var maxPlayersTag = $('#max_players')
var statusTag = $('#status')
var playersListTag = $('#players_list')

const lobby = $('#lobby')
const game = $('#game')
// game.hide()

let max_players;
let n_players_now;
let players;
let status;

const socketio = io()

socketio.emit('check_client_data', game_data)

socketio.on('error', (data) => {
    console.log(data.error)

    error_tag.text(data.error)
})

socketio.on('login_success', () => {
    console.log('login effettuato')

    socketio.emit('game_info', (game_data) => {
        console.log(game_data)

        max_players = game_data.max_players
        n_players_now = game_data.n_players_now
        players = game_data.players
        status = game_data.status

        if (status === "started") {
            // il gioco è in esecuzione
            show_game_table()
        } else {
            nPlayersNowTag.text(n_players_now)
            maxPlayersTag.text(max_players)
            statusTag.text(status)
            playersListTag.text(players)
        }
    })
})

socketio.on('game_starting', (data) => {
    statusTag.text(data.msg)
})

socketio.on('start_game', () => {
    show_game_table()

    console.log('game avviato')
})

function show_game_table() {
    lobby.hide()
    game.show()

    let players = ['antonio', 'marco', 'gino', 'paolo', 'sesso']

    const table = new Table(players, 3)
    table.buildTable()


}

// socketio.on('show_game_table', ()=>{
//
// })