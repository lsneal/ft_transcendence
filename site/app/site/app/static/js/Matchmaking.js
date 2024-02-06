function JoinGameOnline() {
    // fetch(`joinPong`, {
        // headers:{
            // 'Accept': 'application/json',
            // 'X-Requested-With': 'XMLHttpRequest',
        // },
    // })
    // .then((response) => response.json())
    // .then(data => {
        // startGame(data.id)
        // return data;
    // })
    
    //fetch('/api/user', {
    //    method: "GET",
    //    headers:{
    //        'Accept': 'application/json',
    //        'X-Requested-With': 'XMLHttpRequest',
    //    },
    //})
    //.then((response) => response.json())
    //.then(data => {
    //    console.log(data.jwt)
    //})


    fetch("/games/", {
            method: "POST",
            body: "player1: p1 player2: p2",
    })
    .then((response) => response.json())
    .then(data => {
        console.log("game ", data.id)
    })

}

//async function JoinGameOnline() {
//
//}