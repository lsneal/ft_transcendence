async function EventGetQRCode() {
    var Modal2faAcif = new bootstrap.Modal(document.getElementById('modalActivateOrDeactivateTwoFA'), {
        keyboard: false
    });

    var Modal2faInacif = new bootstrap.Modal(document.getElementById('modaltwoFA'), {
        keyboard: false
    });

    try {
        const response = await fetch('https://localhost/api/users/activate2fa/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
      
        console.log('message: ', data.url);
        if (data.message === 'error') {
            Modal2faAcif.show();
        } 
        else if (!Modal2faAcif._isShown) {
            var qrcode = document.createElement("img");
            qrcode.src = data.url;
            var imgElement = document.getElementById("2FA-link");
            imgElement.src = qrcode.src;
            Modal2faInacif.show();
        }
    } catch (error) {
        alert('Erreur de déconnexion');
    }
}   