function JoinGameOnline() {

    fetch("/api/joinGame/", {
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

    fetch("/api/joinGame/", {
        method: "POST",
    })
    .then((response) => response.json())
    .then(data => {
        gameId = data.id;
        console.log("gameId =", gameId)
        startGameLocal(gameId)
    })
}