async function send2facode() {

    let myModalEl = document.getElementById('modalEmail');
    let modal = bootstrap.Modal.getInstance(myModalEl);

    const code1 = document.getElementById('codelog1').value;
    const code2 = document.getElementById('codelog2').value;
    const code3 = document.getElementById('codelog3').value;
    const code4 = document.getElementById('codelog4').value;
    const code5 = document.getElementById('codelog5').value;
    const code6 = document.getElementById('codelog6').value;


    let myModal2FA = document.getElementById('modallogin2fa');
    let modal2fa = bootstrap.Modal.getInstance(myModal2FA);

    const totalcode = code1 + code2 + code3 + code4 + code5 + code6;
    const formData = { totp: totalcode };
    console.log('totalcode', totalcode);
try {
    const response = await fetch('https://localhost/api/users/2fa/', {
        method: 'POST',
        mode: "cors",
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    }).then((response) => response.json())
    .then((data) =>{
        if (data.message == 'success'){
            console.log('data.message: ', data.message)
            modal2fa.hide();
            window.history.pushState(null, "Profile", "/profile/");
            window.dispatchEvent(new Event('popstate'));
        }
        else{
            console.log('data.message: ', data.message);
            const errorMessage = 'Wrong Code';
            const errorElement = document.getElementById('error-message-2fa');
            errorElement.innerText = errorMessage;
            errorElement.style.display = 'block';
        }
    });
}
catch (error) {
    alert('An unexepected error occured. Please try again!', error.message);
};

}