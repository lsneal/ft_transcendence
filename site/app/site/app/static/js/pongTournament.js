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

function buildBracket(data) {
    const list = document.getElementById("list");
    list.style.display = 'none';

    fetch("api/UserIdGameView", {
        method: "GET",
    })
    .then((response) => response.json())
    .then(dataUser => {
        let url = `ws://localhost:8001/ws/` + dataUser.id 
        const socket = new WebSocket(url)
        console.log("url socket = ", url)
        playTournament(gameId, socket, data)
    })
    //const bracket = document.getElementById("bracket");
    //for (let i = 0; i < data.nb_user; i += 2)
    //{
    //    bracket.innerHTML += `<div style="background-color:powderblue;">
    //                            <h1>${data.users[i]}<h1>
    //                            <h1>${data.users[i + 1]}<h1>
    //                        </div>`;
    //}
}

function playTournament(gameId, socket) {

}