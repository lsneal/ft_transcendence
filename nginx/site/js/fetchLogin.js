emailGlob = null

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


    const codeInputs = [
        document.querySelector('#codelog1'),
        document.querySelector('#codelog2'),
        document.querySelector('#codelog3'),
        document.querySelector('#codelog4'),
        document.querySelector('#codelog5'),
        document.querySelector('#codelog6')
    ];

    const formData = {
        email: email,
        password: password,
    };

    document.addEventListener('input', function () {
    
        codeInputs.forEach((input, index) => {
            input.addEventListener('input', function (event) {
                // Remplace tout ce qui n'est pas un chiffre par une chaîne vide
                this.value = this.value.replace(/\D/g, '');
    
                // Déplacement automatique vers le champ suivant si la longueur maximale est atteinte
                const maxLength = parseInt(this.getAttribute('maxlength'));
                if (this.value.length >= maxLength) {
                    const nextInput = this.nextElementSibling;
                    if (nextInput && nextInput.tagName === 'INPUT') {
                        nextInput.focus();
                    }
                } else {
                    // Empêcher le déplacement automatique du focus vers le champ suivant
                    event.preventDefault();
                }
            });
    
            input.addEventListener('keydown', function (event) {
                // Vérifie si la touche pressée est la touche "Backspace" et que le champ est vide
                if (event.key === 'Backspace' && this.value.length === 0) {
                    const prevInput = this.previousElementSibling;
                    if (prevInput && prevInput.tagName === 'INPUT') {
                        prevInput.focus();
                        // Empêcher le comportement par défaut du backspace (navigation en arrière)
                        event.preventDefault();
                    }
                }
            });
        });
    });
    
    codeInputs.forEach((input, index) => {
        
        input.addEventListener('input', (event) => {
            const value = event.target.value;
            if (value >= '0' && value <= '9' && value.length >= event.target.maxLength && index < codeInputs.length) {
                if (index < codeInputs.length - 1)
                    codeInputs[index + 1].focus();
            } else if (index > 0) {
                codeInputs[index - 1].focus();
            }
        });
     
    });
    try {
        const response = await fetch('/api/users/login/', {
            method: 'POST',
            mode: "cors",
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        }).then((response) => response.json())
        .then((data) =>{
            if (data.detail === undefined)
            {
                if (data.a2f === true) {
                    emailGlob = formData.email
                    modal.hide();
                    Modal2fa.show();
                }
                else {
                    modal.hide();
                    window.history.pushState(null, "Profile", "/profile/");
                    window.dispatchEvent(new Event('popstate'));
                }
               
            }
            else
            {
                const errorMessage = data.detail;
                const errorElement = document.getElementById('error-message-Login');
                errorElement.innerText = errorMessage;
                errorElement.style.display = 'block'; 
            }

        });
    }
    catch (error) {
      console.error(error);
    };
}