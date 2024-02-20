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
        const response = await fetch('https://localhost/api/register/', {
            method: 'POST',
            mode: "cors",
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        }).then((response) => response.json())
        .then((data) =>{
            console.log(data.email[0]);
            console.log(data);
            if(data.id !== undefined){
                modal.hide();
                window.history.pushState(null, "Register", "/");
                window.dispatchEvent(new Event('popstate'));
            }
            else{
                const errorMessage = data.email[0];
                    const errorElement = document.getElementById('error-message-Register');
                    errorElement.innerText = errorMessage;
                    errorElement.style.display = 'block'; // Assurez-vous que l'élément est affiché
            }

            // If it fails put error in modal 

        });
    }
    catch (error) {
        alert('An unexepected error occured. Please try again!');
    };


    // If error -> Print on the error in the modal ?    Else close modal and redirect (code behind)


}











    

