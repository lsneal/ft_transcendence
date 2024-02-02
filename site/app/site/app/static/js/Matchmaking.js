function JoinGame() {
    fetch(`joinPong`, {
        headers:{
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then((response) => response.json())
    .then(data => {
        startGame(data.id)
        return data;
    })		
}