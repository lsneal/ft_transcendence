

async function EventProfile() {
    
    try {
        const userresponse = await fetch('/api/users/user/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        const userData = await userresponse.json();

        if (userData.detail === "Unauthenticated!") {
            window.history.pushState(null, "Logout", "/");
            window.dispatchEvent(new Event('popstate'));
        }
    } catch (error) {
        alert('Erreur : ' + error.message);
    }
}