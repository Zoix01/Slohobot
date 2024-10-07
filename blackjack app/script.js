let firstCard = 11
let secondCard = 9
let sum = firstCard + secondCard

let liveDraw = false
let blackJack = false
let deadDraw = false
let message = ""

if (sum <= 20) {
    message = "Do you want to draw another card?"
    liveDraw = true
} else if (sum === 21) {
    message = "Congrats, you won the game!"
    blackJack = true
} else {
    message = "Oh no, you lost"
    deadDraw = true
}
console.log(blackJack)
console.log(liveDraw)
console.log(deadDraw)
console.log(message)