
async function EventGetQRCode() {
    try {
        const response = await fetch('https://localhost/api/users/activate2fa/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then((response) => response.json())
        .then((data) =>{
            console.log(data.qr)
            console.log('data.url: ', data.qr)
            var qrcode = document.createElement("img");
            qrcode.src = data.url;
            var imgElement = document.getElementById("2FA-link");
            imgElement.src = qrcode.src;
        });

    } catch (error) {
        alert('Errrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrreur de déconnexion');
    }

    /*window.history.pushState(null, "Profile", "/profile/");
    window.dispatchEvent(new Event('popstate'));*/
}

async function EventActiveTwoFA() {

    const code1 = document.querySelector('#code1').value;
    const code2 = document.querySelector('#code2').value;
    const code3 = document.querySelector('#code3').value;
    const code4 = document.querySelector('#code4').value;
    const code5 = document.querySelector('#code5').value;
    const code6 = document.querySelector('#code6').value;
    const final_code = code1 + code2 + code3 + code4 + code5 + code6;

    console.log(final_code)

    if (final_code.length != 6) {
        alert('Code pas bon');
        return ;
    }

    const formData = {
        totp_code: final_code
    };

    try {
        const response = await fetch('https://localhost/api/users/activate2fa/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        }).then((response) => response.json())
        .then((data) => {
            console.log(data);
            console.log(data.pseudo);
        });
    }
    catch (error) {
        alert('Error code')
    }
}