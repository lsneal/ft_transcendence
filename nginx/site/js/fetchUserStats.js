
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
        console.log('data.img: ', data.img)
        const prc_win = (data.victory / data.nb_game) *100
     // Mettre à jour les éléments HTML avec les données récupérées
     const pieChartData = {
        labels: ['Victoires', 'Parties Jouées'],
        datasets: [{
            data: [prc_win, data.nb_game - data.victory],
            backgroundColor: ['#F2AFEF', '#7360DF']
        }]
    };

    // Récupérer le contexte du canvas
    const ctx = document.getElementById('myChart').getContext('2d');
    console.log('ctx', ctx);
    // Créer le pie chart
    const myPieChart = new Chart(ctx, {
        type: 'pie',
        data: pieChartData
    });

    } catch (error) {
        alert('Erreur: ' + error.message);
    }
}