function startGameLocal(gameId) {
    if (document.getElementById("resultMatch") != null)
        document.getElementById("resultMatch").style.display = 'none';
    let button = document.getElementById("ButtonStart")
    button.style.display = 'none'

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
        playGameLocal(gameId, socket)
    })
}

let keyP1 = undefined;
let keyP2 = undefined;
var Interval = undefined

function gameLoop(gameId, socket)
{
    console.log("Je suis dedans")
    if (keyP1 != undefined)
    {
        socket.send(JSON.stringify({
            'game':'in progress',
            'moov': keyP1,
            'gameId': gameId,
            'typeParty': 'game'
        }))
    }
    if (keyP2 != undefined)
    {
        socket.send(JSON.stringify({
            'game':'in progress',
            'moov': keyP2,
            'gameId': gameId,
            'typeParty': 'game'
        }))
    }
}

function playGameLocal(gameId, socket)
{ 
    let button = document.getElementById("ButtonStart")

    let numRight = 250;
    let numLeft = 250;
    
    let winner = null

    let leftBar = document.getElementById("leftBox")
    let ball = document.getElementById("ball")
    let rightBar = document.getElementById("rightBox")

    socket.onopen = () => {
        socket.send(JSON.stringify({
            'game':'local',
            'moov':'none',
            'gameId': gameId,
            'typeParty': 'game'
        }))

        socket.send(JSON.stringify({
            'game':'start',
            'moov':'none',
            'gameId': gameId,
            'typeParty': 'game'
        }))
        Interval = setInterval(() => {
            gameLoop(gameId, socket);
        }, 60)
    }

    document.addEventListener("keyup", function (e) {
        e.preventDefault();
        if  (e.key === "w" || e.key === "s")
            keyP1 = undefined;
    })

    document.addEventListener("keydown", function (e) {
        if (socket.readyState !== WebSocket.CLOSED)
        {
            e.preventDefault();
            if  (e.key === "w" || e.key === "s")
            {
                keyP1 = e.key;    
            }
        }
    })

    document.addEventListener("keyup", function (e) {
        e.preventDefault();
        if (e.key === "ArrowUp" || e.key === "ArrowDown")
        {
            keyP2 = undefined;
        }
    })

    document.addEventListener("keydown", function (e) {
        if (socket.readyState !== WebSocket.CLOSED)
        {
            e.preventDefault();
            if (e.key === "ArrowUp" || e.key === "ArrowDown")
                keyP2 = e.key;
        }
    })


    socket.onmessage = function (event) {
        let data = JSON.parse(event.data)
        if (data.type === "game")
        {
            if (data.moov === "ArrowUp" || data.moov === "ArrowDown")
            {
                numRight = data.rightBoxTop.toString();
                rightBar.style.top = numRight + "px";
            }
            if (data.moov === "w" || data.moov === "s")
            {
                numLeft = data.leftBoxTop.toString();
                leftBar.style.top = numLeft + "px";
            }
            if (data.moov === "ball")
            {
                if (window.innerWidth < 1288)
                {
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
            if (data.time == '-1')
            {
                document.getElementById("time").style.display = 'none';
            }
        }

    }
    socket.onclose = () => {
        keyP1 = undefined;
        keyP2 = undefined;
        if (Interval != undefined)
            clearInterval(Interval);
        Interval = undefined
        resultMatch = document.getElementById("resultMatch")
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
        button.style.display = 'block';
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