

async function EventProfile() {
    try {
        const response = await fetch('/api/users/user/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then((response) => response.json())
        .then((data) =>{
        });

    } catch (error) {
        alert('Erreur de déconnexion');
    }

    /*window.history.pushState(null, "Profile", "/profile/");
    window.dispatchEvent(new Event('popstate'));*/
}