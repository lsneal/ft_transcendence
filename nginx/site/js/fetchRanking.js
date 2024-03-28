async function getRankingPlayers() {
    try {
        const response = await fetch('api/dashboard/player-ranking/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
         console.log(response);
        if (!response.ok) {
            throw new Error('Erreur de recuperation du classement des joueurs');
        }

        const data = await response.json();


        data.sort((a, b) => (b.victory / b.nb_game *100) - (a.victory / b.nb_game *100));

        const tbody = document.querySelector('#scoreboard-table tbody');

        tbody.innerHTML = '';

        data.forEach((player, index) => {
            const prc_win = player.nb_game === 0 ? 0 : (player.victory / player.nb_game) * 100;

            const row = document.createElement('tr');

            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${player.pseudo}</td>
                <td>${player.victory}</td>
                <td>${player.nb_game}</td>
                <td>${prc_win.toFixed(2)}%</td>
            `;

            tbody.appendChild(row);
        });

    } catch (error) {
        alert('Erreur de recuperation du classement des joueurs: ' + error.message);
    }
}

