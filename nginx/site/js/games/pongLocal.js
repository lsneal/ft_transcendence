function startGameLocal(gameId) {
    if (document.getElementById("time") != null)
        document.getElementById("time").style.display = 'none';
    if (document.getElementById("crown") != null)
        document.getElementById("crown").style.display = 'none';
    let button = document.getElementById("ButtonStart")
    button.style.display = 'none'
    if (document.getElementById("ball") != null)
    {
        document.getElementById("ball").style.height = "35px";
        document.getElementById("ball").style.width = "35px";
    }

    if (!gameId)
        return ;
    gameId = Number(gameId)

    fetch("/api/users/user/", {
        method: "GET",
    })
    .then((response) => response.json())
    .then(data => {
        let url = `wss://10.13.249.106/api/pong/ws/` + data.data.id 
        const socket = new WebSocket(url)
        playGameLocal(gameId, socket)
    })
}

function gameLoopLocal(gameId, socket)
{
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

let keyP1 = undefined;
let keyP2 = undefined;
var IntervalLocal = undefined;

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
        IntervalLocal = setInterval(() => {
            gameLoopLocal(gameId, socket);
        }, 30)
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
                if (document.getElementById("scoreP1") == null || document.getElementById("scoreP2") == null)
                    socket.close()
                else
                {
                    document.getElementById("scoreP1").innerHTML = data.scoreP1;
                    document.getElementById("scoreP2").innerHTML = data.scoreP2;
                }
                if (data.scoreP1 == 5)
                {
                    winner = "p1";
                    res = 250;    
                    res = res.toString();
                    leftBar.style.top = res + "px";
                    rightBar.style.top = res + "px";
                }
                if (data.scoreP2 == 5)
                {
                    winner = "p2";
                    res = 250;    
                    res = res.toString();
                    leftBar.style.top = res + "px";
                    rightBar.style.top = res + "px";
                }        
            }
        }
        if (data.type === "time" && document.getElementById("time"))
        {
            document.getElementById("time").style.display = 'block';
            document.getElementById("time").style.fontSize = '7.0rem';
            document.getElementById("time").style.left = '50%';
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
        if (IntervalLocal != undefined)
            clearInterval(IntervalLocal);
        IntervalLocal = undefined

        if (document.getElementById("time") != null)
        {
            document.getElementById("time").style.display = 'block';
            document.getElementById("crown").style.display = 'block';
            if (winner == 'p1')
                document.getElementById("time").innerHTML = `Joueur1 Wins`;
            if (winner == 'p2')
                document.getElementById("time").innerHTML = `Joueur2 Wins`;
            document.getElementById("time").style.fontSize = 'xxx-large';
            document.getElementById("time").style.left = '35%';

            document.getElementById("scoreP1").innerHTML = 0
            document.getElementById("scoreP2").innerHTML = 0
            button.style.display = 'block';
            document.getElementById("ball").style.width = "100px";
            document.getElementById("ball").style.height = "100px";
        }
        ball.style.top = "240px";
        ball.style.left ="45%";
        ball.style.animation = "none";

    }
}