async function EventLogin42 () {

    try {
        const response = fetch('https://localhost/api/users/login42/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        }).then((response) => response.json())
        .then((data) =>{
            window.location.href = data[0];
        });
    }
    catch (error) {
      console.log(error);
    };

}



