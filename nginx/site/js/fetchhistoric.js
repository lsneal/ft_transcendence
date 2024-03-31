async function getHistoricOnline () {

    const myModalEl = document.getElementById('modalBurger');
    const modal = bootstrap.Modal.getInstance(myModalEl);


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
        modal.hide();
        const tbody = document.querySelector('#historicTable tbody');
        tbody.innerHTML = '';
        for (let i = 1; i < dataDashboard.game_data.length; i++) {
            const game = dataDashboard.game_data[i];
            let result;
            if (game.marked_point === 5){
                result = 'victoire'
            }else{
                result = 'defaite'
            }
            const row = document.createElement('tr');
            row.innerHTML = `
                <td id="table-primaire">${game.opponent}</td>
                <td id="table-secondaire">${game.marked_point}</td>
                <td id="table-tertiaire">${game.conceded_point}</td>
                <td id="table-quaternaire">${result}</td>
            `;
            tbody.appendChild(row);
        }
    } catch (error) {
    }
}  