async function EventRegister () {

    console.log("test");

    const email = document.querySelector('#email').value;
    const pseudo = document.querySelector('#pseudo').value;
    const password = document.querySelector('#password').value;

    let myModalEl = document.getElementById('modalRegistrer');
    let modal = bootstrap.Modal.getInstance(myModalEl);


    if (!email || !pseudo ||!password) {
        //alert('Veuillez remplir tous les champs !');
        modal.hide();
        return; 
    }

    const formData = {
        email: email,
        pseudo: pseudo,
        password: password,
    };

    try {
        const response = await fetch('https://api.localhost/register/', {
            method: 'POST',

            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        if (response.ok) {
            alert('Register OK!');
        } else {
            const errorMessage = await response.json();
            alert('Erreur ' + errorMessage.email[0]); 
        }
    }
    catch (error) {
        alert('An unexepected error occured. Please try again!');
    };


    // If error -> Print on the error in the modal ?    Else close modal and redirect (code behind)

    modal.hide();
    window.history.pushState(null, "Register", "/");
    window.dispatchEvent(new Event('popstate'));

}











    

