function startGame(gameId) {

    gameId = Number(gameId)
    
    let numRight = 250;
    let numLeft = 250;
    
    let leftBar = document.getElementById("leftBox")
    let ball = document.getElementById("ball")
    let rightBar = document.getElementById("rightBox")

    let url = `ws://localhost:8001/ws/` + gameId //game.id
    const socket = new WebSocket(url)
    
    socket.onopen = () => {
        socket.send(JSON.stringify({
             'game':'start',
             'moov':'none',
             'gameId': gameId,
        }))
        console.log("le jeux commence = '", gameId, "'");

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
        console.log("Data:", data)
        if (data.type === "game")
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
                console.log("reiceve ball " , data.moov)
                document.getElementById("scoreP1").innerHTML = data.scoreP1;
                document.getElementById("scoreP2").innerHTML = data.scoreP2;
            }
        }
    }	
}
