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

    let gameId = -1;
    fetch("/api/joinGame/", {
        method: "POST",
    })
    .then((response) => response.json())
    .then(data => {
        gameId = data.id;
    })
    if (gameId != -1)
        startGame(gameId)
}