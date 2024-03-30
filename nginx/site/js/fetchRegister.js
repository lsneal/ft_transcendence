async function EventRegister () {


    const email = document.querySelector('#email').value;
    const pseudo = document.querySelector('#pseudo').value;
    const password = document.querySelector('#password').value;
    const confirmPassword = document.querySelector('#ConfirmPassword').value;


    let myModalEl = document.getElementById('modalRegistrer');
    let modal = bootstrap.Modal.getInstance(myModalEl);


    if (!email || !pseudo ||!password || !confirmPassword) {
        //alert('Veuillez remplir tous les champs !');
        const errorMessage = 'Empty fields';
        const errorElement = document.getElementById('error-message-Register');
        errorElement.innerText = errorMessage;
        errorElement.style.display = 'block';
        return; 
    }
    if (password != confirmPassword){
        const errorMessage = 'Not Same Password';
        const errorElement = document.getElementById('error-message-Register');
        errorElement.innerText = errorMessage;
        errorElement.style.display = 'block';
        return;
    }
 
    const formData = {
        email: email,
        pseudo: pseudo,
        password: password,
    };

    try {
        const response = await fetch('/api/users/register/', {
            method: 'POST',
            mode: "cors",
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        }).then((response) => response.json())
        .then((data) =>{
            if(data.id !== undefined){
                fetch('/api/dashboard/connectUser/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        pseudo: data.pseudo,
                    })
                });
                modal.hide();
                window.history.pushState(null, "Register", "/");
                window.dispatchEvent(new Event('popstate'));
            } 
            else {
                errorMessage = "";
                if (data.pseudo)
                    errorMessage = data.pseudo;
                else if (data.email)
                    errorMessage = data.email;
                else
                    errorMessage = data.password    
                const errorElement = document.getElementById('error-message-Register');
                errorElement.innerText = errorMessage;
                errorElement.style.display = 'block'; // Assurez-vous que l'élément est affiché
            }


        });
    }
    catch (error) {
        alert(error)
    };




}











    

