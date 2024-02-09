function startGame(gameId) {
    let button = document.getElementById("JoinGameOnline");
    
    button.style.display = 'none'
    if (!gameId)
        return ;
    gameId = Number(gameId)

    let numRight = 250;
    let numLeft = 250;
    
    let winner = null

    let leftBar = document.getElementById("leftBox")
    let ball = document.getElementById("ball")
    let rightBar = document.getElementById("rightBox")

    let url = `ws://localhost:8001/ws/` + gameId
    const socket = new WebSocket(url)
    console.log("url socket = ", url)
    socket.onopen = () => {
        console.log("send on open");
        socket.send(JSON.stringify({
            'game':'none',
            'moov':'none',
            'gameId': gameId,
        }))

        window.addEventListener("keydown", function (e) {
            if (e.key === "w" || e.key === "s" || e.key === "ArrowUp" || e.key === "ArrowDown")
            {
                socket.send(JSON.stringify({
                    'game':'in progress',
                    'moov':e.key,
                    'gameId': gameId,
                }))
            }
        })
    }

    socket.onmessage = function (event) {
        let data = JSON.parse(event.data)
        if (data.type == "start")
        {
            console.log("caca")
            socket.send(JSON.stringify({
                'game':'start',
                'moov':'none',
                'gameId': gameId,
            }))
        }
        else if (data.type === "game")
        {
            if (data.moov === "ArrowUp" || data.moov === "ArrowDown")
            {
                numLeft = data.leftBoxTop.toString();
                numRight = data.rightBoxTop.toString();
                leftBar.style.top = numLeft + "px";
                rightBar.style.top = numRight + "px";
            }
            if (data.moov === "ball")
            {
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
    }
    socket.onclose = () => {
        resultMatch = document.getElementById("resultMatch")
        if (winner == 'p1')
            resultMatch.innerHTML = "And the winner is Player1"
        if (winner == 'p2')
            resultMatch.innerHTML = "And the winner is Player2"
        document.getElementById("scoreP1").innerHTML = 0
        document.getElementById("scoreP2").innerHTML = 0
        button.style.display = 'block';
    }
}
