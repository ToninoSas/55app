class Table {
    constructor(players, handSize, socketio) {
        this.players = players
        this.handSize = handSize
        this.socketio = socketio

        this.top = $('#top')
        this.center = $('#center')
        this.bottom = $('#bottom')

        this.hands = []

        this.setupFor4 = {
            0: 0,
            1: -90,
            2: 0,
            3: 90
        }

        this.setupFor5 = {
            0: 0,
            1: -90,
            2: 0,
            3: 0,
            4: 90
        }
    }

    #buildBets() {
        let puntoGrande = new CircularIndicator(70)
        let puntiPiccoli = [
            new CircularIndicator(10),
            new CircularIndicator(10),
            new CircularIndicator(10)]

        let bets_div = $('<div class="bets-div"></div>')

        bets_div.append(puntoGrande, puntiPiccoli)
        return bets_div
    }

    #buildHands() {
        let size = this.players.length

        // emit socket event for player hand cards
        const cards = [1, 2, 3]

        for (let j = 0; j < size; j++) {
            let rotation = size === 4 ? this.setupFor4[j] : this.setupFor5[j]
            let hand = Hand.buildHand(cards, rotation, this.players[j])
            this.hands.push(hand)
        }
        const bets = this.#buildBets()

        if (size === 4) {
            this.bottom.append(this.hands[0])
            this.center.append(this.hands[1])
            this.top.append(this.hands[2])
            this.center.append(bets)
            this.center.append(this.hands[3])
        } else {
            this.bottom.append(this.hands[0])
            this.center.append(this.hands[1])
            this.top.append(this.hands[2])
            this.top.append(this.hands[3])
            this.center.append(bets)
            this.center.append(this.hands[4])
        }
    }

    buildTable() {
        this.buildChat()
        this.#buildHands()
        this.buildPlayerData()
    }


    buildPlayerData(){
        let player_data = $('<div id="player-data"></div>')

        let player_actions = $('<div></div>')
        let player_budget = $('<div></div>')

        const score_label = $('<span id="player-score"></span>')
        const passa_action = $('<div class="player-action">Passa</div>')
        const punta_action = $('<div class="player-action">Punta</div>')

        player_budget.append(new CircularIndicator(1000, 'player-budget'))
        player_actions.append(score_label, passa_action, punta_action)

        player_data.append(player_budget, player_actions)

        this.bottom.append(player_data)
    }

    buildChat(){
        let chat = $('<div id="chat"></div>')

        let messages = ['E il turno di player 1', 'Player 1 ha passato']

        for (let msg in messages){
            chat.append($('<p>'+ messages[msg] + '</p>'))
        }

        this.bottom.append(chat)
        this.bottom.append($('<div style="width: 225px"></div>'))

    }
}