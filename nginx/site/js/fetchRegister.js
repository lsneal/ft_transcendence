

  // Écoutez l'événement de soumission du formulaire
  async function EventRegister () {

      // Récupérez les valeurs des champs de formulaire
      const email = document.querySelector('#email').value;
      const pseudo = document.querySelector('#pseudo').value;
      const password = document.querySelector('#password').value;

      console.log('Valeurs des champs:', email, pseudo, password);

      // Construisez l'objet à envoyer
      const formData = {
          email: email,
          pseudo: pseudo,
          password: password,
      };

      console.log('Valeur fu form', JSON.stringify(formData));

      try {
          // Effectuez une requête POST à l'API
          const response = await fetch('http://localhost:3000/register/', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify(formData)
          });
          console.log('reponse de lapi:', response);

          // Vérifiez si la requête a réussi
          if (response.ok) {
              // Affichez un message de succès
          console.log('Reussi');
            } else {
              // Affichez un message d'erreur
              console.error('Erreur lors de lenvoie', response.statusText)
            }
      } catch (error) {
          console.error('Erreur lors de l\'envoi des informations :', error);
      }
  };
