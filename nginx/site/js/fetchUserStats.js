async function getUserStats() {
    try {
        let dataDashboard;
        const userresponse = await fetch('/api/users/user/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            } 
        });
        const userData = await userresponse.json();
        console.log('data :', userData.data.email);

        const responseDashboard = await fetch('/api/dashboard/connectUser/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: userData.data.email,
                pseudo: userData.data.pseudo,
            })
        });
        dataDashboard = await responseDashboard.json();
        drawChart(dataDashboard);
        console.log('Données : ', dataDashboard);
       
    } catch (error) {
        alert('Erreur : ' + error.message);
    }
}

async function drawChart(dataDashboard) {
    const prc_win = (dataDashboard.victory / dataDashboard.nb_game) * 100;

    const pieChartData = {
        labels: ['Victoires', 'Défaites'],
        datasets: [{
            data: [prc_win, 100 - prc_win],
            backgroundColor: ['#F2AFEF', '#7360DF']
        }]
    };

    const canvas = document.getElementById('myChart');
    const ctx = canvas.getContext('2d');
    const radius = Math.min(canvas.width, canvas.height) / 2;

    // Fonction pour dessiner le graphique en camembert
    function drawPieSlice(ctx, centerX, centerY, radius, startAngle, endAngle, color) {
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, radius, startAngle, endAngle);
        ctx.closePath();
        ctx.fill();
    }

    // Fonction pour dessiner le graphique
    function drawChart() {
        let startAngle = 0;
        for (let i = 0; i < pieChartData.datasets[0].data.length; i++) {
            const data = pieChartData.datasets[0].data[i];
            const color = pieChartData.datasets[0].backgroundColor[i];
            const sliceAngle = 2 * Math.PI * (data / 100);
            const endAngle = startAngle + sliceAngle;
            drawPieSlice(ctx, canvas.width / 2, canvas.height / 2, radius, startAngle, endAngle, color);
            startAngle = endAngle;
        }
    }

    drawChart();

    // Afficher les pourcentages dans la légende en dessous du graphique
    const legend = document.createElement('div');
    legend.classList.add('legend');
    legend.innerHTML = `
        <span class="legend-item">${pieChartData.labels[0]}: ${prc_win.toFixed(2)}%</span>
        <span class="legend-item">${pieChartData.labels[1]}: ${(100 - prc_win).toFixed(2)}%</span>
    `;
    canvas.parentNode.insertBefore(legend, canvas.nextSibling);

    // Mettre à jour les barres de progression
    document.getElementById('nbVictoiresBar').style.width = prc_win + '%';
    document.getElementById('nbPartiesBar').style.width = '100%'; // La largeur de la barre pour le nombre de parties est toujours à 100%

    // Mettre à jour les titres des barres de progression
    document.getElementById('nbVictoiresBar').title = `Nombre de victoires : ${dataDashboard.victory}`;
    document.getElementById('nbPartiesBar').title = `Nombre de parties jouées : ${dataDashboard.nb_game}`;
}
