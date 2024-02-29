async function EventLogin42 () {

    let myModalEl = document.getElementById('modalLogin');
    let modal = bootstrap.Modal.getInstance(myModalEl);

    try {
        const response = fetch('https://localhost/api/users/login42/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        }).then((response) => response.json())
        .then((data) =>{
            const popup = window.open(data, '_blank', "left=800,top=100,width=480,height=480");
            const checkPopup = setInterval(() => {
                if (popup.window.location.href.includes("https://localhost/profile/")) {
                    popup.close()
                    modal.hide();
                    window.history.pushState(null, "Profile", "/profile/");
                    window.dispatchEvent(new Event('popstate'));
                }
                if (!popup || !popup.closed) return;
                clearInterval(checkPopup);
             }, 500);
        });
    }
    catch (error) {
      console.log(error);
    };

}



