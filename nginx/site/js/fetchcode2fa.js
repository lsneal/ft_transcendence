async function send2facode() {


    const code1 = document.getElementById('codelog1');
    const code2 = document.getElementById('codelog2');
    const code3 = document.getElementById('codelog3');
    const code4 = document.getElementById('codelog4');
    const code5 = document.getElementById('codelog5');
    const code6 = document.getElementById('codelog6');

    const totalcode = code1 + code2 + code3 + code4 + code5 + code6;

    const formData = { totalcode: totalcode };

try {
    const response = await fetch('api/users/2fa/', {
        method: 'POST',
        mode: "cors",
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    }).then((response) => response.json())
    .then((data) =>{
        console.log('data; ');
    });
}
catch (error) {
    alert('An unexepected error occured. Please try again!', error.message);
};

}