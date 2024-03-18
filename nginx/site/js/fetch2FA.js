async function EventGetQRCode() {
    var Modal2faAcif = new bootstrap.Modal(document.getElementById('modalActivateOrDeactivateTwoFA'), {
        keyboard: false
    });

    var Modal2faInacif = new bootstrap.Modal(document.getElementById('modaltwoFA'), {
        keyboard: false
    });

    try {
        const response = await fetch('/api/users/activate2fa', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
        console.log('message: ', data.message);
        if (data.message === 'error') {
            console.log('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa');
            Modal2faAcif.show();
        } else if (!Modal2faAcif._isShown) {
            console.log('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb');
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
