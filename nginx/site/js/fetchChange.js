async function EventChange () {
    const pseudo = document.querySelector('#ChangePseudo').value;
    const  oldpassword  = document.querySelector('#OldPassword').value;
    const  password  = document.querySelector('#ChangePassword').value;
    const  confirmpassword  = document.querySelector('#ConfirmChangePassword').value;

   // const twoFA = document.querySelector('#').value;

    if(oldpassword == password && oldpassword != null){
      const errorMessage = 'No changes made';
      const errorElement = document.getElementById('error-message-nochange');
      errorElement.innerText = errorMessage;
      errorElement.style.display = 'block';
      return;
    }
    else if(password != confirmpassword){
      const errorMessage = 'Not Same Password';
      const errorElement = document.getElementById('error-message-Confirmchange');
      errorElement.innerText = errorMessage;
      errorElement.style.display = 'block';
      return;
    }

    const formData = {
        pseudo: pseudo,
        oldpassword: oldpassword,
        password: password,
    };
    
    const jsonString = JSON.stringify(formData);

    
    const url = 'https://localhost/api/user/';

    const options = {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: jsonString
      };

      fetch(url, options)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error ${response.status}`);
        }
        return response.json();
      })
      .then(updatedData => {
        console.log('Data updated:', updatedData);
      })

}



