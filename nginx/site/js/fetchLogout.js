

async function EventLogout() {

    const myModalEl = document.getElementById('modalBurger');
    const modal = bootstrap.Modal.getInstance(myModalEl);
    try {
        const response = await fetch('/api/users/logout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        }).then((response) => response.json())
        .then((data) =>{
            modal.hide();
            window.history.pushState(null, "Logout", "/");
            window.dispatchEvent(new Event('popstate'));
        });

    } catch (error) {
        
    }


}