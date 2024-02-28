function startGameOnline(gameId) {
    let button2 = document.getElementById("JoinGameOnline");

    button2.style.display = 'none'
    if (!gameId)
        return ;
    gameId = Number(gameId)

    fetch("https://localhost/api/pong/UserIdGameView", {//TODO: fetch sur user
        method: "GET",
    })
    .then((response) => response.json())
    .then(data => {
        let url = `wss://localhost/api/pong/ws/` + data.id 
        const socket = new WebSocket(url)
        playGameOnline(gameId, socket)
    })
}

function playGameOnline(gameId, socket)
{ 
    let button2 = document.getElementById("JoinGameOnline");

    let numRight = 250;
    let numLeft = 250;
    
    let winner = null

    let leftBar = document.getElementById("leftBox")
    let ball = document.getElementById("ball")
    let rightBar = document.getElementById("rightBox")


    socket.onopen = () => {
        socket.send(JSON.stringify({
            'game':'start',
            'moov':'none',
            'gameId': gameId,
            'typeParty': 'game'
        }))

        window.addEventListener("keydown", function (e) {
            if (e.key === "w" || e.key === "s" || e.key === "ArrowUp" || e.key === "ArrowDown")
            {
                socket.send(JSON.stringify({
                    'game':'in progress',
                    'moov':e.key,
                    'gameId': gameId,
                    'typeParty': 'game'
                }))
            }
        })
    }

    socket.onmessage = function (event) {
        let data = JSON.parse(event.data)
        if (data.type === "game")
        {
            if (data.moov === "ArrowUp" || data.moov === "ArrowDown")
            {
                //TODO: changer les valeurs suivant la taille de fenetre
                numLeft = data.leftBoxTop.toString();
                numRight = data.rightBoxTop.toString();
                leftBar.style.top = numLeft + "px";
                rightBar.style.top = numRight + "px";
            }
            if (data.moov === "ball")
            {
                //TODO: changer les valeurs suivant la taille de fenetre
                ball.style.top = data.posY.toString() + "px";
                ball.style.left = data.posX.toString() + "px";
                document.getElementById("scoreP1").innerHTML = data.scoreP1;
                document.getElementById("scoreP2").innerHTML = data.scoreP2;
                if (data.scoreP1 == 5)
                    winner = "p1";
                if (data.scoreP2 == 5)
                    winner = "p2";
            }
        }
        if (data.type === "time")
            document.getElementById("time").innerHTML = data.time;
    }
    socket.onclose = () => {
        resultMatch = document.getElementById("resultMatch")
        if (winner == 'p1')
            resultMatch.innerHTML = "And the winner is Player1"
        if (winner == 'p2')
            resultMatch.innerHTML = "And the winner is Player2"
        document.getElementById("scoreP1").innerHTML = 0
        document.getElementById("scoreP2").innerHTML = 0
        //TODO: changer les valeurs suivant la taille de fenetre
        posY = 250
        posX = 499
        ball.style.top = posY.toString() + "px";
        ball.style.left = posX.toString() + "px";
        button2.style.display = 'block';
    }
}