

async function EventLogout() {
    try {
        const response = await fetch('https://localhost/api/logout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        }).then((response) => response.json())
        .then((data) =>{
            // Logout shouldn't fail for now, we'll see later

        });

    } catch (error) {
        alert('Erreur de déconnexion');
        
    }

    window.history.pushState(null, "Logout", "/");
    window.dispatchEvent(new Event('popstate'));
}