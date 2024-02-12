

async function EventLogout() {
    try {
        const response = await fetch('http://localhost:3000/logout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            console.log('Ok', response.text())
            alert('Déconnexion réussie!');

        } else {
            const errorMessage = await response.json();
            alert('Erreur de déconnexion: ' + errorMessage.detail);
        }
    } catch (error) {
        alert('Erreur de déconnexion');
    }
}