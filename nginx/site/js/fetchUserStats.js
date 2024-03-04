
async function getUserStats() {
    try {
        const response = await fetch('https://localhost/api/users/stats/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (!response.ok) {
            throw new Error('Erreur de récupération des statistiques utilisateur');
        }

        const data = await response.json();
        console.log('data.victory: ', data.victory);
        console.log('data.nb_game: ', data.nb_game);
        const partiesJouees = data.nb_game;
        const victoires = data.victory;
        const percentageVictoire = (victoires / partiesJouees) * 100;
        console.log('partie jouee,  victory', partiesJouees, victoires);

    } catch (error) {
        alert('Erreur: ' + error.message);
    }
}