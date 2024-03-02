function JoinGameOnline() {

    fetch("/api/pong/joinGame/", {
        method: "POST",
    })
    .then((response) => response.json())
    .then(data => {
        gameId = data.id;
        startGameOnline(gameId)
    })
}

function JoinGameLocal() {

    fetch("/api/pong/joinGame/", {
        method: "POST",
    })
    .then((response) => response.json())
    .then(data => {
        gameId = data.id;
        startGameLocal(gameId)
    })
}