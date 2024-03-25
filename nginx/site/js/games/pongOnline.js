player1 = null;
player2 = null;

function startGameOnline(gameId, player, pseudo, name1, name2) {
    if (document.getElementById("time") != null)
        document.getElementById("time").style.display = 'none';
    if (document.getElementById("crown") != null)
        document.getElementById("crown").style.display = 'none';
    let button2 = document.getElementById("JoinGameOnline");

    button2.style.display = 'none'
    if (!gameId)
        return ;
    gameId = Number(gameId)
    
    fetch("/api/users/user/", {
            method: "GET",
        })
        .then((response) => response.json())
        .then(data => {
            let url = `wss://localhost/api/pong/ws/` + data.data.id 
            const socket = new WebSocket(url)
            player1 = name1
            player2 = name2
            playGameOnline(gameId, socket, pseudo, player)
        })
}

function playGameOnline(gameId, socket, pseudo, player)
{ 
    let button2 = document.getElementById("JoinGameOnline");

    let numRight = 250;
    let numLeft = 250;
    
    let winner = null

    let leftBar = document.getElementById("leftBox")
    let ball = document.getElementById("ball")
    let rightBar = document.getElementById("rightBox")


    socket.onopen = () => {
        console.log("player1 = ", player1, "player2 = ", player2);
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
                {
                    winner = "p1";
                    UserStatsGame(pseudo, 'p1', player, 'p2', data.scoreP1, data.scoreP2);
                }
                if (data.scoreP2 == 5)
                {
                    winner = "p2";
                    UserStatsGame(pseudo, 'p2', player, 'p1', data.scoreP1, data.scoreP2);
                }
            }
        }
        if (data.type === "time")
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
        
        document.getElementById("time").style.display = 'block';
        document.getElementById("crown").style.display = 'block';
        if (winner == 'p1')
            document.getElementById("time").innerHTML = `Joueur1 gagne`;
        if (winner == 'p2')
            document.getElementById("time").innerHTML = `Joueur2 gagne`;
        document.getElementById("time").style.fontSize = 'xxx-large';
        document.getElementById("time").style.left = '38%';

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
        document.getElementById("time").innerHTML = ``;
    }
}

async function UserStatsGame(pseudo, winner, player, looser, p1Score, p2Score) {
    if (winner === player || looser === player)
    {   
        console.log("wine = ", winner);
        console.log("loose = ", looser)
        await  fetch("/api/users/user/", {
            method: "GET",
        })
        .then((response) => response.json())
        .then(data => {            
            if (data.data.pseudo === pseudo && winner === player)
            {
                const conceded_point = (player == 'p1') ?  p2Score : p1Score
                const marked_point = (player == 'p1') ?  p1Score : p2Score
                const opponent = (player == 'p1') ? player2 : player1  
                console.log(conceded_point, marked_point, opponent)
                fetch('/api/dashboard/connectUser/', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'pseudo': pseudo, 
                        'gameEnd': 'true',
                        'win' : 'true',
                    },
                    body: JSON.stringify({
                        'conceded_point': conceded_point,
                        'marked_point': marked_point,
                        'opponent': opponent
                    })
                });
            }
            else if (data.data.pseudo === pseudo && looser === player)
            {

                const conceded_point = (player == 'p1') ?  p2Score : p1Score
                const marked_point = (player == 'p1') ?  p1Score : p2Score
                const opponent = (player == 'p1') ? player2 : player1
                console.log(conceded_point, marked_point, opponent)
                fetch('/api/dashboard/connectUser/', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'pseudo': pseudo, 
                        'gameEnd': 'true',
                        'win' : 'false',
                    },
                    body: {
                        'conceded_point': conceded_point,
                        'marked_point': marked_point,
                        'opponent': opponent 
                    }
                });
            }
            return
        })
    }
}
