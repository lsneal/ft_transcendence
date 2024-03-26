async function getHistoricOnline () {

    let myModalEl = document.getElementById('modalBurger');
    let modal = bootstrap.Modal.getInstance(myModalEl);


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
        console.log(dataDashboard.pseudo)
        console.log(dataDashboard.game_data)
        modal.hide();
        const tbody = document.querySelector('#historicTable tbody');
        tbody.innerHTML = '';
        for (let i = 1; i < dataDashboard.game_data.length; i++) {
            const game = dataDashboard.game_data[i];
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${game.opponent}</td>
                <td>${game.marked_point}</td>
                <td>${game.conceded_point}</td>
            `;
            tbody.appendChild(row);
        }
    } catch (error) {
        alert('Erreur : ' + error.message);
    }
}  