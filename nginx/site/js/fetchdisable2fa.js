async function EventDisableTwoFA() {
    console.log('aaaaaaaaaaaaaaaaaaaaaaaaab');

    let myModalEl = document.getElementById('modalActivateOrDeactivateTwoFA');
    let modal = bootstrap.Modal.getInstance(myModalEl);



    try {
        const response = await fetch('https://localhost/api/users/activate2fa/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        const data = await response.json();
        console.log(data.message);
        modal.hide();
    } catch (error) {
        console.error('Erreur lors de la désactivation du 2FA :', error);
    }
}

