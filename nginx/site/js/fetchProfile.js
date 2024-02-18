

async function EventProfile() {
    try {
        const response = await fetch('https://localhost/api/user/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            console.log('Ok', response.text())

        } else {
            // If it fails, that means the user isn't connected or his cookies expired, 
            // so put error and redirect him to Home (or refresh token ?)
        }
    } catch (error) {
        alert('Erreur de déconnexion');
    }

    /*window.history.pushState(null, "Profile", "/profile/");
    window.dispatchEvent(new Event('popstate'));*/
}