async function EventLogin () {



    const email = document.querySelector('#emailLogin').value;
    const password = document.querySelector('#PasswordLogin').value;


  var myModalEl = document.getElementById('modalEmail');
  var modal = bootstrap.Modal.getInstance(myModalEl);

  console.log(modal);


  if (!email || !password) {
      alert('Veuillez remplir tous les champs !');
      modal.hide();
      return; 
  }

    const formData = {
        email: email,
        password: password,
    };



    try {
        const response = await fetch('http://localhost:3000/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
          alert('Login OK!');
      } else {
          const errorMessage = await response.json();
          alert('Erreur ' + errorMessage.detail); 
          }
      }
      catch (error) {
          alert('Erreur');
      };

      modal.hide();

  }

