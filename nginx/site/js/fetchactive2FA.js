async function EventActiveTwoFA() {


    let myModalEl = document.getElementById('modaltwoFA');
    let modal = bootstrap.Modal.getInstance(myModalEl);


    const code1 = document.getElementById('code1').value;
    const code2 = document.getElementById('code2').value;
    const code3 = document.getElementById('code3').value;
    const code4 = document.getElementById('code4').value;
    const code5 = document.getElementById('code5').value;
    const code6 = document.getElementById('code6').value;
    const final_code = code1 + code2 + code3 + code4 + code5 + code6;
    console.log('code 1', code1);
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
            alert('Bien ouej');
            modal.hide();
            window.history.pushState(null, "Profile", "/profile/");
            window.dispatchEvent(new Event('popstate'));
        });
    }
    catch (error) {
        alert('Error code')
    }
}