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

        const responseDashboard = await fetch('/api/dashboard/connectUser/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'pseudo': userData.data.pseudo 
            },
        });
        dataDashboard = await responseDashboard.json();
        drawChart(dataDashboard);
    } catch (error) {
    }
}

async function drawChart(dataDashboard) {
    const nbGames = dataDashboard.nb_game;
    const nbVictories = dataDashboard.victory;
    const nbDefaite = nbGames - nbVictories;
    if (nbGames === 0) {
        
        const legend = document.querySelector('.legend');
        if (legend) {
            legend.style.display = 'none';
        }
        
        document.getElementById('nbVictoiresBar').style.display = 'none';
        document.getElementById('nbPartiesBar').style.display = 'none';
        document.getElementById('nbDefaiteBar').style.display = 'none';

        
        const errorMessage = "No game played";
        const errorElement = document.getElementById('errormessageStat');
        errorElement.innerText = errorMessage;
        errorElement.style.display = 'block'; 
        return; 
    }

    


    document.getElementById('myChart').style.display = 'block';
    



    const existingLegend = document.querySelector('.legend');
    if (existingLegend) {
        existingLegend.parentNode.removeChild(existingLegend);
    }


    let legends = document.getElementById('legend');
    if (legends) {
        legends.style.display = 'block';
    }
    
    document.getElementById('nbVictoiresBar').style.display = 'block';
    document.getElementById('nbPartiesBar').style.display = 'block';
    document.getElementById('nbDefaiteBar').style.display = 'block';


    const prc_win = (nbVictories / nbGames) * 100;
    const prc_loose = 100 - prc_win;
    const pieChartData = {
        labels: ['Victories', 'Loses'],
        datasets: [{
            data: [prc_win, 100 - prc_win],
            backgroundColor: ['#A3C9AA', '#9B4444']
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

    const legend = document.createElement('div');
    legend.classList.add('legend');
    if (prc_win == NaN){
        prc_win = 0
        prc_loose = 0
    }    
    legend.innerHTML = `
        <span class="legend-item">${pieChartData.labels[0]}: ${prc_win.toFixed(2)}%</span>
        <span class="legend-item">${pieChartData.labels[1]}: ${(100 - prc_win).toFixed(2)}%</span>
    `;
    canvas.parentNode.insertBefore(legend, canvas.nextSibling);

    document.getElementById('nbVictoiresBar').style.width = prc_win + '%';
    document.getElementById('nbDefaiteBar').style.width = prc_loose + '%';
    document.getElementById('nbPartiesBar').style.width = '100%'; 

    document.getElementById('nbVictoiresBar').title = `Victories : ${nbVictories}`;
    document.getElementById('nbDefaiteBar').title = `Number of losses : ${nbDefaite}`;
    document.getElementById('nbPartiesBar').title = `Number of games : ${nbGames}`;

   
}