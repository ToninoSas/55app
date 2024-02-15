class Hand {
    constructor(playername, size, rotation) {
        this.playername = playername
        this.size = size
        this.rotation = rotation
        this.cards = []
    }

    static buildHand(cards, rotation, playername) {
        let hand_div = $('<div></div>')
        let hand_cards = $('<div></div>')

        for (let i = 0; i < cards.length; i++) {
            let card_div = $('<div></div>')
            card_div.addClass('card')

            hand_cards.append(card_div)
            hand_cards.addClass('hand-cards')
        }

        let label = $('<span></span>')
        label.text(playername)
        label.addClass('player-name-label')

        hand_div.append(label)
        hand_div.append(hand_cards)
        hand_div.css("transform", `rotate(${rotation}deg)`)
        hand_div.addClass('hand')

        return hand_div
    }
}

class CircularIndicator{
    constructor(value, id) {
        let circle = $('<div id=' + id + '></div>')
        circle.addClass('circular-indicator')
        circle.text(value)
        return circle
    }
}