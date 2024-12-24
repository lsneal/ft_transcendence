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
   
    if (document.getElementById("ball") != null)
    {
        document.getElementById("ball").style.height = "30px";
        document.getElementById("ball").style.width = "30px";
    }



    fetch("/api/users/user/", {
            method: "GET",
        })
        .then((response) => response.json())
        .then(data => {
            let url = `wss://10.13.249.106/api/pong/ws/` + data.data.id 
            const socket = new WebSocket(url)
            let player1 = name1
            let player2 = name2
            if (player1 != player2)
            {
                playGameOnline(gameId, socket, pseudo, player)
            }
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
    let eventWin;

    function sendToSocket(e)
    {
        if (e.key === "ArrowUp" || e.key === "ArrowDown")
        {
            socket.send(JSON.stringify({
                'game':'in progress',
                'moov':e.key,
                'gameId': gameId,
                'typeParty': 'game'
            }))
        }
    }

    socket.onopen = () => {
        socket.send(JSON.stringify({
            'game':'start',
            'moov':'none',
            'gameId': gameId,
            'typeParty': 'game'
        }))
        
        window.addEventListener("keydown", sendToSocket, false);
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
                if (document.getElementById("scoreP1") == null || document.getElementById("scoreP2") == null)
                {
                    socket.close()
                }
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
                    UserStatsGame(pseudo, 'p1', player, 'p2', data.scoreP1, data.scoreP2, gameId);
                    socket.close()
                }
                if (data.scoreP2 == 5)
                {
                    winner = "p2";
                    res = 250;    
                    res = res.toString();
                    leftBar.style.top = res + "px";
                    rightBar.style.top = res + "px";
                    UserStatsGame(pseudo, 'p2', player, 'p1', data.scoreP1, data.scoreP2, gameId);
                    socket.close()
                }
            }
        }
        if (data.type === "time")
        {
            displayName(gameId)
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
        window.removeEventListener("keydown", sendToSocket, false);
        if (document.getElementById("time") != null && document.getElementById("player2"))
        {
            document.getElementById("player1").innerHTML = ``
            document.getElementById("player2").innerHTML = ``
            document.getElementById("time").style.display = 'block';
            document.getElementById("crown").style.display = 'block';
            document.getElementById("time").style.fontSize = 'xxx-large';
            document.getElementById("time").style.left = '35%';

            document.getElementById("scoreP1").innerHTML = 0
            document.getElementById("scoreP2").innerHTML = 0
            button2.style.display = 'block';
            document.getElementById("ball").style.width = "100px";
            document.getElementById("ball").style.height = "100px";
        }
        ball.style.top = "240px";
        ball.style.left ="45%";
        ball.style.animation = "none";
        

     
    }
}

async function  UserStatsGame(pseudo, winner, player, looser, p1Score, p2Score, gameId) {
    
    let player1 = null
    let player2 = null
    await fetch("/api/pong/getGame/" + gameId, {
        method: "GET",
    })
    .then((response) => response.json())
    .then(data => {
        player1 = data.player1_name
        player2 = data.player2_name
        document.getElementById("time").style.display = 'block';
        if (data.player2 == winner)
            document.getElementById("time").innerHTML = `${data.player2_name} Wins`
        if (data.player1 == winner)
            document.getElementById("time").innerHTML = `${data.player1_name} Wins`
    })
    if (winner === player || looser === player)
    {   
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
                fetch('/api/dashboard/connectUser/', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'pseudo': pseudo, 
                        'gameEnd': 'true',
                        'win' : 'false',
                    },
                    body: JSON.stringify({
                        'conceded_point': conceded_point,
                        'marked_point': marked_point,
                        'opponent': opponent 
                    })
                });
            }
            return
        })
    }
}


async function displayName(gameId) {
    await fetch("/api/pong/getGame/" + gameId, {
        method: "GET",
    })
    .then((response) => response.json())
    .then(data => {
        document.getElementById("player1").innerHTML = data.player1_name
        document.getElementById("player2").innerHTML = data.player2_name
    })
    
}