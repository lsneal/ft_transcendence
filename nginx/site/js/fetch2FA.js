
async function EventGetQRCode() {
    try {
        const response = await fetch('https://localhost/api/users/activate2fa/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then((response) => response.json())
        .then((data) =>{
            var qrcode = document.createElement("img");
            qrcode.src = data.url;
            var imgElement = document.getElementById("2FA-link");
            imgElement.src = qrcode.src;
        });

    } catch (error) {
        alert('Errrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrreur de déconnexion');
    }

}

