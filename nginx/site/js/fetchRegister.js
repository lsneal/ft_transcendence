async function EventRegister () {



      const email = document.querySelector('#email').value;
      const pseudo = document.querySelector('#pseudo').value;
      const password = document.querySelector('#password').value;


    var myModalEl = document.getElementById('modalRegistrer');
    var modal = bootstrap.Modal.getInstance(myModalEl);

    console.log(modal);


    if (!email || !pseudo ||!password) {
        alert('Veuillez remplir tous les champs !');
        modal.hide();
        return; 
    }

      const formData = {
          email: email,
          pseudo: pseudo,
          password: password,
      };



      try {
          const response = await fetch('http://localhost:3000/register/', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify(formData)
          });

          if (response.ok) {
            alert('Register OK!');
        } else {
            const errorMessage = await response.json();
            alert('Erreur ' + errorMessage.email[0]); 
            }
        }
        catch (error) {
            alert('Erreur');
        };
        modal.hide();

    }



    

