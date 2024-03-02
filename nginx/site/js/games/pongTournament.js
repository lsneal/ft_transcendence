let arrPlayer = new Array();

function insertUsers() {
    console.log("oo");
}

function CreateTournament() {

    let button3 = document.getElementById("tournament");
    let users = document.getElementById("users");
    
    button3.style.display = 'none';
    users.style.display = 'block';

    let nbPlayer = document.getElementById("nbP");
    nbPlayer = Number(nbPlayer.value);

    
    //let inputs = document.getElementById("inputs");
    //inputs.style.display = 'block';
    //inputs.innerHTML = ``
    //for (let i = 0; i < nbPlayer; i++)
    //{
    //    inputs.innerHTML += `<input type="text" name="name" id="name${i}"/>`;
    //    
    //}
}

function getName() {
    
    for (let i = 0; i < 16; i++)
    {
        if (document.getElementById(`name${i}`) == null)
            break ;
        let name = document.getElementById(`name${i}`);
        arrPlayer[i] = name.value
    }

    fetch("/api/pong/tournament", { // faire un check du nombre de nom donne et le nombre de user
        method: "POST",
        headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
                    "users": arrPlayer,
                    "nb_user": arrPlayer.length
                }),
    })
    .then((response) => response.json())
    .then(data => {
        buildBracket(data);
    })
}

function buildBracket(value) {
    const list = document.getElementById("list");
    let inputs = document.getElementById("inputs");
    list.style.display = 'none';
    inputs.style.display = 'none';

    fetch("/api/pong/joinGame/", {
        method: "POST",
    })
    .then((response) => response.json())
    .then(data => {
        beforeStart(data.id, value)
    })
}

function beforeStart(gameId, value) {
    fetch("/api/pong/UserIdGameView", {
        method: "GET",
    })
    .then((response) => response.json())
    .then(dataUser => {
        let url = `wss://localhost/api/pong/ws/` + dataUser.id 
        const socket = new WebSocket(url)
        playTournament(gameId, socket, value)
    })
}

function playTournament(gameId, socket, tournament) {
    
    let leftBar = document.getElementById("leftBox")
    let ball = document.getElementById("ball")
    let rightBar = document.getElementById("rightBox")

    let button3 = document.getElementById("tournament");

    socket.onopen = () => {
        socket.send(JSON.stringify({
            'game':'tournament',
            'moov': 'none',
            'tournamentId':tournament.id,
            'gameId':gameId,
            'users':tournament.users,
            'nb_user':tournament.nb_user,
            'typeParty': 'tournament'
        }))
        socket.send(JSON.stringify({
            'game':'start',
            'moov':'none',
            'gameId': gameId,
            'typeParty': 'tournament'
        }))

        window.addEventListener("keydown", function (e) {
            if (e.key === "w" || e.key === "s" || e.key === "ArrowUp" || e.key === "ArrowDown")
            {
                socket.send(JSON.stringify({
                    'game':'in progress',
                    'moov':e.key,
                    'gameId': gameId,
                    'typeParty': 'tournament'
                }))
            }
        })
    }

    socket.onmessage = function (event) {
        let data = JSON.parse(event.data)
        if (data.type === "time")
        {
            document.getElementById("time").style.display = 'block';
            document.getElementById("time").innerHTML = data.time;
            if (data.time == '4')
            {
                document.getElementById("time").style.display = 'none';
            }
        }
        if (data.type === "players")
        {
            const bracket = document.getElementById("bracket");
            bracket.innerHTML = `<div style="background-color:powderblue;">
                           <h1>${data.player1}<h1>
                           <h1>${data.player2}<h1>
                       </div>`;
        }
        if (data.type === "end")
        {
            const bracket = document.getElementById("bracket");
            bracket.innerHTML = ``
            resultMatch = document.getElementById("resultMatch")
            resultMatch.innerHTML = "And the winner is " + data.winner
            document.getElementById("scoreP1").innerHTML = 0
            document.getElementById("scoreP2").innerHTML = 0
            return
        }
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
                if (data.scoreP2 == 5 || data.scoreP1 == 5)
                {
                    socket.send(JSON.stringify({
                        'game':'tournamentInProgress',
                        'moov': 'none',
                        'tournamentId':tournament.id,
                        'gameId':gameId,
                        'typeParty': 'tournament'
                    }))
                    if (socket.readyState != WebSocket.CLOSED)
                    {
                        socket.send(JSON.stringify({
                            'game':'start',
                            'moov':'none',
                            'gameId': gameId,
                            'typeParty': 'tournament'
                        }))
                    }            
                }
            }
        }
    }

    socket.onclose = () => {
        const list = document.getElementById("list");
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
        ball.style.top = posY.toString() + "px";
        ball.style.left = posX.toString() + "px";
        button3.style.display = 'block';
        list.style.display = 'block';
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