async function getUserStats() {
    try {
        const response = await fetch('https://localhost/api/users/stats/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        }).then((response) => response.json())
        .then((data) =>{
            console.log('data.victory: ', data.victory);
            console.log('data.nb_game: ', data.nb_game);
            
            const partiesJouees = data.nb_game;
            const victoires = data.victory;
            const percentageVictoire = (victoires / partiesJouees) * 100;
            console.log ('partie jouee,  victory', partiesJouees, victoires);
            // document.getElementById('victoires').style = `rotate(${percentageVictoire}deg)`;

            document.getElementById('pie-chart').style.background = "conic-gradient(#7360DF 0% " + percentageVictoire + "%, #F2AFEF " + percentageVictoire + "% 100%)";

        });

    } catch (error) {
        alert('Errrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrreur de déconnexion');
    }

}