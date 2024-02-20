async function EventLogin () {

    const email = document.querySelector('#emailLogin').value;
    const password = document.querySelector('#PasswordLogin').value;

    let myModalEl = document.getElementById('modalEmail');
    let modal = bootstrap.Modal.getInstance(myModalEl);


    if (!email || !password) {
        alert('Veuillez remplir tous les champs !');
        modal.hide();
        return; 
    }

    /*var getCookie = function(name) {
      var re = new RegExp(name + "=([^;]+)");
      var value = re.exec(document.cookie);
      return (value != null) ? unescape(value[1]) : null;
    };*/

    const formData = {
        email: email,
        password: password,
    };

    try {
        const response = await fetch('https://localhost/api/login/', {
            method: 'POST',
            mode: "cors",
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        }).then((response) => response.json())
        .then((data) =>{
            console.log(data.detail);
            if (data.detail === undefined)
            {
                modal.hide();
                window.history.pushState(null, "Profile", "/profile/");
                window.dispatchEvent(new Event('popstate'));
            }
            else
            {
                const errorMessage = data.detail || 'suce ma bite';
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



