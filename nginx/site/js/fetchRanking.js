getRankingPlayers() {
    try {
        const response = await fetch('https://localhost/api/users/rank/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (!response.ok) {
            throw new Error('Erreur de récupération du classement des joueurs');
        }

        const data = await response.json();
        
        console.log('Classement des joueurs:', data);

        // Calculer prc_win pour chaque joueur
        data.forEach(player => {
            player.prc_win = player.nb_game === 0 ? 0 : (player.victory / player.nb_game) * 100;
        });

        // Trier les joueurs par leur pourcentage de victoire (prc_win)
        data.sort((a, b) => b.prc_win - a.prc_win);

        // Sélectionner le corps du tableau
        const tbody = document.querySelector('#scoreboard-table tbody');

        // Réinitialiser le contenu du corps du tableau
        tbody.innerHTML = '';

        // Ajouter chaque joueur au tableau avec son numéro de classement
        data.forEach((player, index) => {
            // Créer une nouvelle ligne pour le joueur
            const row = document.createElement('tr');

            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${player.pseudo}</td>
                <td>${player.victory}</td>
                <td>${player.nb_game}</td>
                <td>${player.prc_win}%</td>
            `;
            
            tbody.appendChild(row);
        });

    } catch (error) {
        alert('Erreur de récupération du classement des joueurs: ' + error.message);
    }
}
