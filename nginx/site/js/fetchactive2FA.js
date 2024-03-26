async function EventActiveTwoFA() {

    let myModalEl = document.getElementById('modaltwoFA');
    let modal = bootstrap.Modal.getInstance(myModalEl);

    const code1 = document.querySelector('#code1').value;
    const code2 = document.querySelector('#code2').value;
    const code3 = document.querySelector('#code3').value;
    const code4 = document.querySelector('#code4').value;
    const code5 = document.querySelector('#code5').value;
    const code6 = document.querySelector('#code6').value;
    const final_code = code1 + code2 + code3 + code4 + code5 + code6;

    console.log(final_code)

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
            if(data.message === "success"){
                const errorMessage = '2FA Actif';
                const errorElement = document.getElementById('errormactive2fa');
                errorElement.innerText = errorMessage;
                modal.hide();
            }else{
                const errorMessage = 'Wrong Code';
                const errorElement = document.getElementById('errormactive2fa');
                errorElement.innerText = errorMessage;
                errorElement.style.display = 'block';
            }
        });

        const data = await response.json();
        console.log(data);
        console.log(data.pseudo);
    }catch (error) {
        console.error(error.message)
      
    }
}
