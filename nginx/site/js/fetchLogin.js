async function EventLogin () {

    const email = document.querySelector('#emailLogin').value;
    const password = document.querySelector('#PasswordLogin').value;

    let myModalEl = document.getElementById('modalEmail');
    let modal = bootstrap.Modal.getInstance(myModalEl);

    //console.log(modal);

    if (!email || !password) {
        alert('Veuillez remplir tous les champs !');
        modal.hide();
        return; 
    }

    const formData = {
        email: email,
        password: password,
    };

    try {
        const response = await fetch('https://api.localhost/login/', {
            method: 'POST',
            mode: "cors",
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        console.log(response);

        if (response.ok) {
          //alert('Login OK!');
        } else {
          const errorMessage = await response.json();
          alert('Erreur ' + errorMessage.detail); 
        }
    }
    catch (error) {
      alert('Erreur');
    };

    modal.hide();

    window.history.pushState(null, "Profile", "/profile/");
    window.dispatchEvent(new Event('popstate'));
}



