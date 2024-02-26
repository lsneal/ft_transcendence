function JoinGameOnline() {

    fetch("/api/games/joinGame/", {
        method: "POST",
    })
    .then((response) => response.json())
    .then(data => {
        gameId = data.id;
        console.log("gameId =", gameId)
        startGameOnline(gameId)
    })
}

function JoinGameLocal() {
    console.log("PUTEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")

    fetch("https://localhost/api/pong/joinGame/", {
        method: "POST",
    })
    .then((response) => response.json())
    .then(data => {
        console.log("PUTEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
        gameId = data.id;
        console.log("gameId =", gameId)
        startGameLocal(gameId)
    })
}