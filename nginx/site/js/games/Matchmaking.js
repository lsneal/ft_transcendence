function JoinGameOnline() {

    fetch("/api/users/user/", {
        method: "GET",
    })
    .then((response) => response.json())
    .then(user => {
        fetch("/api/pong/joinGame/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                //'pseudo': res.data.pseudo
            },
            body: JSON.stringify({'pseudo': user.data.pseudo}),
        })
        .then((response) => response.json())
        .then(data => {
            gameId = data.id;
            player1 = null;
            player2 = null;
            if (data.player2 == 'null')
            {
                player1 = user.data.pseudo
                startGameOnline(gameId, 'p1', player1, data.player1_name, data.player2_name)
            }
            else
            {
                player2 = user.data.pseudo
                startGameOnline(gameId, 'p2', player2 , data.player1_name, data.player2_name)
            }
        })
    })
}

async function JoinGameLocal() {

    await fetch("/api/pong/joinGame/", {
        method: "POST",
    })
    .then((response) => response.json())
    .then(data => {
        gameId = data.id;
        startGameLocal(gameId)
    })
}