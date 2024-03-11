async function EventLogin () {

    const email = document.querySelector('#emailLogin').value;
    const password = document.querySelector('#PasswordLogin').value;

    let myModalEl = document.getElementById('modalEmail');
    let modal = bootstrap.Modal.getInstance(myModalEl);


    var Modal2fa = new bootstrap.Modal(document.getElementById('modallogin2fa'), {
        keyboard: false
      });

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
        const response = await fetch('/api/users/login/', {
            method: 'POST',
            mode: "cors",
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        }).then((response) => response.json())
        .then((data) =>{
            if (data.detail === undefined)
            {
                try {
                    const response =  fetch('/api/users/login/', {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                        }
                    }).then((response) => response.json())
                    .then((data) =>{
                    console.log('message: ', data.message);
                    if (data.message == 'True'){
                        console.log('active');
                        Modal2fa.show();
                        

                    }    
                    else{
                        console.log('pas active');
                        modal.hide();
                        window.history.pushState(null, "Profile", "/profile/");
                        window.dispatchEvent(new Event('popstate'));
                    }
                    });
                }
                catch (error) {
                  console.log('Erreur');
                };
             
            }
            else
            {
                const errorMessage = data.detail;
                const errorElement = document.getElementById('error-message-Login');
                errorElement.innerText = errorMessage;
                errorElement.style.display = 'block'; // Assurez-vous que l'élément est affiché
            }

            // If it fails put error in modal 


            // You can look at that doc to know everything you can use with you response https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
            // Here I use https://developer.mozilla.org/en-US/docs/Web/API/Response/json
            // To retrieve and parse the errors correctly

        });
    }
    catch (error) {
      console.log('Erreur');
    };

  
    // If login fail then don't do that and add the message in the modal with js
    
}



