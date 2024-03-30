async function EventGetQRCode() {
    const codeInputs = [
        document.querySelector('#code1'),
        document.querySelector('#code2'),
        document.querySelector('#code3'),
        document.querySelector('#code4'),
        document.querySelector('#code5'),
        document.querySelector('#code6')
    ];
    
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
    var Modal2faAcif = new bootstrap.Modal(document.getElementById('modalActivateOrDeactivateTwoFA'), {
        keyboard: false
    });

    var Modal2faInacif = new bootstrap.Modal(document.getElementById('modaltwoFA'), {
        keyboard: false
    });

    try {
        const response = await fetch('https://localhost/api/users/activate2fa/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
      
        if (data.message === 'error') {
            Modal2faAcif.show();
        } 
        else if (!Modal2faAcif._isShown) {
            var qrcode = document.createElement("img");
            qrcode.src = data.url;
            var imgElement = document.getElementById("2FA-link");
            imgElement.src = qrcode.src;
            Modal2faInacif.show();
        }
    } catch (error) {
    }
}   