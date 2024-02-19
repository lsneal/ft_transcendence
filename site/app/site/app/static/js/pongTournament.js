function CreateTournament() {

    let button = document.getElementById("ButtonStart")
    let button2 = document.getElementById("JoinGameOnline");
    let button3 = document.getElementById("tournament");

    button.style.display = 'none'
    button2.style.display = 'none'
    button3.style.display = 'none'

    let nbPlayer = document.getElementById("nbP")
    nbPlayer = Number(nbPlayer.value)
    
    const list = document.getElementById("list");
    for (let i = 0; i < nbPlayer; i++)
    {
        list.innerHTML += `<input type="text" name="name" id="name${i}"/>`;
    }
}

function getName() {
    let arrPlayer = new Array();
    for (let i = 0; i < 16; i++)
    {
        if (document.getElementById(`name${i}`) == null)
            break ;
        let name = document.getElementById(`name${i}`);
        arrPlayer[i] = name.value
    }

    fetch("api/tournament", { // faire un check du nombre de nom donne et le nombre de user
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
        console.log(data)
    })
}

function buildBracket(value) {
    const list = document.getElementById("list");
    list.style.display = 'none';

    fetch("/api/joinGame/", {
        method: "POST",
    })
    .then((response) => response.json())
    .then(data => {
        beforeStart(data.id, value)
    })
}

function beforeStart(gameId, value) {
    fetch("api/UserIdGameView", {
        method: "GET",
    })
    .then((response) => response.json())
    .then(dataUser => {
        let url = `ws://localhost:8001/ws/` + dataUser.id 
        const socket = new WebSocket(url)
        console.log("url socket = ", url)
        playTournament(gameId, socket, value)
    })
}

function playTournament(gameId, socket, tournament) {
    
    socket.onopen = () => {
        console.log("tournament id =", tournament.id)
        socket.send(JSON.stringify({
            'game':'tournament',
            'moov': 'none',
            'tournamentId':tournament.id,
            'gameId':gameId,
            'users':tournament.users,
            'nb_user':tournament.nb_user
        }))
        console.log("tournament create")
        socket.send(JSON.stringify({
            'game':'start',
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
        if (data.type === "players")
        {
            console.log("receive message players")
            const bracket = document.getElementById("bracket");
            bracket.innerHTML += `<div style="background-color:powderblue;">
                           <h1>${data.player1}<h1>
                           <h1>${data.player2}<h1>
                       </div>`;
        }
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
    }
}