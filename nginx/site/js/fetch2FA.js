
async function EventActiveTwoFA() {
    try {
        const response = await fetch('https://localhost/api/users/activate2fa', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then((response) => response.json())
        .then((data) =>{
            console.log(data);
            console.log(data.pseudo);
            console.log(data.url)
            const errorMessage = data.url;
            const errorElement = document.getElementById('2FA-link');
            errorElement.innerText = errorMessage;
            errorElement.style.display = 'block'; // A
            // If it fails, that means the user isn't connected or his cookies expired, 
            // so put error and redirect him to Home (or refresh token ?) 

        });

    } catch (error) {
        alert('Errrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrreur de déconnexion');
    }

    /*window.history.pushState(null, "Profile", "/profile/");
    window.dispatchEvent(new Event('popstate'));*/
}