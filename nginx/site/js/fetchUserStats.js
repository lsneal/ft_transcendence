async function getUserStats() {
    try {
        const response = await fetch('/api/dashboard/user-stats/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error('Erreur de récupération des statistiques utilisateur');
        }

        const data = await response.json();
        console.log('data: ', data);

        // Calculer le pourcentage de victoires
        const prc_win = (data.victory / data.nb_game) * 100;

        // Créer les données pour le pie chart
        const pieChartData = {
            labels: ['Victoires', 'Défaites'],
            datasets: [{
                data: [prc_win, 100 - prc_win],
                backgroundColor: ['#F2AFEF', '#7360DF']
            }]
        };

        // Récupérer le contexte du canvas
        const ctx = document.getElementById('myChart').getContext('2d');

        // Créer le pie chart
        const myPieChart = new Chart(ctx, {
            type: 'pie',
            data: pieChartData
        });

        // Mettre à jour les barres de progression
        document.getElementById('nbVictoiresBar').style.width = prc_win + '%';
        document.getElementById('nbPartiesBar').style.width = '100%'; // La largeur de la barre pour le nombre de parties est toujours à 100%

        // Mettre à jour les titres des barres de progression
        document.getElementById('nbVictoiresBar').title = `Nombre de victoires: ${data.victory}`;
        document.getElementById('nbPartiesBar').title = `Nombre de parties jouées: ${data.nb_game}`;

    } catch (error) {
        alert('Erreur: ' + error.message);
    }
}
