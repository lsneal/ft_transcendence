let arrPlayer = new Array();

function CreateTournament() {
    if (document.getElementById("resultMatch") != null)
        document.getElementById("resultMatch").style.display = 'none';
    let nbPlayer = document.getElementById("nbP");
    let button3 = document.getElementById("tournament");
    let users = document.getElementById("users");
    
    button3.style.display = 'none';
    users.style.display = 'block';

    nbPlayer = nbPlayer.value.split(' ');
    nbPlayer = Number(nbPlayer[0]);
    for (let i = 0; i < nbPlayer; i+=2)
    {
        users.innerHTML += `<div class="row mb-4">
                                <div class="col">
                                    <input type="text" class="form-control" id="name${i}" placeholder="nom du joueur">
                                </div>
                                <div class="col">
                                    <input type="text" class="form-control" id="name${i + 1}" placeholder="nom du joueur">  
                                </div>
                            </div>`   
    }
    users.innerHTML += `
        <div class="d-flex align-items-center justify-content-center">
            <button type="button" onclick="getName(${nbPlayer})" id="button_tournament" class="btn btn-primary btn-lg lign-items-center" >Commencer le tournoi</button>
        </div>
            `
}

function getName(nbPlayer) 
{    
    if (document.getElementById("error") != null)
        document.getElementById("error").style.display = 'none';
    for (let i = 0; i < nbPlayer; i++)
    {
        let name = document.getElementById(`name${i}`);
        if (name === null || name.value === "")
            break ;
        arrPlayer[i] = name.value
    }
    if (nbPlayer == arrPlayer.length)
    {
        let users = document.getElementById("users");
        users.innerHTML = ``;
        users.style.display = 'none';
        fetch("/api/pong/tournament", {
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
    else
        document.getElementById("error").style.display = 'block';

}

function buildBracket(value) {
    const list = document.getElementById("list");
    list.style.display = 'none';

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

let keyP1 = undefined;
let keyP2 = undefined;
var Interval = undefined;
function gameLoop(gameId, socket)
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
        if (data.type === "time")
        {
            document.getElementById("time").style.display = 'block';
            document.getElementById("time").innerHTML = data.time;
            if (data.time == '0')
            {
                document.getElementById("time").style.display = 'none';
            }
        }
        if (data.type === "players")
        {
            console.log("tournois = ", data.tournamentUsers);
            const bracket = document.getElementById("bracket");
            if (data.player1 != undefined)
            {    
                bracket.innerHTML = `<div class="d-flex align-items-center justify-content-center">
                                        <h1 class="p-3 mb-2 bg-dark text-white rounded"> ${data.player1}    vs    ${data.player2}</h1>
                                    </div>`;
            }
            else
            {
                const bracket = document.getElementById("bracket");
                bracket.innerHTML = ``
            }
        }
        if (data.type === "end")
        {
            const bracket = document.getElementById("bracket");
            bracket.innerHTML = ``
            let resultMatch = document.getElementById("resultMatch");
            resultMatch.style.display = 'block';
            resultMatch.innerHTML += `Le gagnant du tournoi est ${data.winner}`
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
        keyP1 = undefined;
        keyP2 = undefined;
        if (Interval != undefined)
            clearInterval(Interval);
        Interval = undefined
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