function startGameOnline(gameId) {
    if (document.getElementById("resultMatch") != null)
        document.getElementById("resultMatch").style.display = 'none';
    let button2 = document.getElementById("JoinGameOnline");

    button2.style.display = 'none'
    if (!gameId)
        return ;
    gameId = Number(gameId)

    fetch("/api/pong/UserIdGameView", {//TODO: fetch sur user
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
            if (e.key === "ArrowUp" || e.key === "ArrowDown")
            {
                socket.send(JSON.stringify({
                    'game':'in progress',
                    'moov':e.key,
                    'gameId': gameId,
                    'typeParty': 'game'
                }))
            }
        })
        
        window.addEventListener("keydown", function (e) {
            if (e.key === "w" || e.key === "s")
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
                numLeft = data.leftBoxTop.toString();
                numRight = data.rightBoxTop.toString();
                leftBar.style.top = numLeft + "px";
                rightBar.style.top = numRight + "px";
            }
            if (data.moov === "ball")
            {
                if (window.innerWidth < 1288)
                {
                    //data.posY /= 2;
                    data.posX /= 2;
                    ball.style.top = data.posY.toString() + "px";
                    ball.style.left = data.posX.toString() + "px";
                }
                else
                {
                    ball.style.top = data.posY.toString() + "px";
                    ball.style.left = data.posX.toString() + "px";
                }
                document.getElementById("scoreP1").innerHTML = data.scoreP1;
                document.getElementById("scoreP2").innerHTML = data.scoreP2;
                if (data.scoreP1 == 5)
                    winner = "p1";
                if (data.scoreP2 == 5)
                    winner = "p2";
            }
        }
        if (data.type === "time")
        {
            document.getElementById("time").style.display = 'block';
            document.getElementById("time").innerHTML = data.time;
            if (data.time == '4')
            {
                document.getElementById("time").style.display = 'none';
            }
        }
    }
    socket.onclose = () => {
        let resultMatch = document.getElementById("resultMatch");
        resultMatch.style.display = 'block';
        if (winner == 'p1')
            resultMatch.innerHTML += "Le gagnant est Joueur1"
        if (winner == 'p2')
            resultMatch.innerHTML += "Le gagnant est Joueur2"
        document.getElementById("scoreP1").innerHTML = 0
        document.getElementById("scoreP2").innerHTML = 0
        posY = 250
        posX = 499
        if (window.innerWidth < 1288)
        {
            posX /= 2;
            ball.style.top = posY.toString() + "px";
            ball.style.left = posX.toString() + "px";
        }
        else
        {
            ball.style.top = posY.toString() + "px";
            ball.style.left = posX.toString() + "px";
        }
        button2.style.display = 'block';
        document.getElementById("time").innerHTML = '0';
    }
}

function reportWindowSize() {
    if (window.innerWidth < 1288)
    {
        document.getElementById("game").style.width = "500px";
    }
    else
    {
        document.getElementById("game").style.width = "1000px";
    }
}

window.onresize = reportWindowSize;