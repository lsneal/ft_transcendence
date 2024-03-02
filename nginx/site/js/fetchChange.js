async function EventChange () {
    const pseudo = document.querySelector('#ChangePseudo').value;
    const  oldpassword  = document.querySelector('#OldPassword').value;
    const  password  = document.querySelector('#ChangePassword').value;
    const  confirmpassword  = document.querySelector('#ConfirmChangePassword').value;

   // const twoFA = document.querySelector('#').value;

    if(oldpassword == password && oldpassword != ''){
      const errorMessage = 'No changes made';
      const errorElement = document.getElementById('error-message-Login');
      errorElement.innerText = errorMessage;
      errorElement.style.display = 'block';
      return;
    }
    else if(password != confirmpassword && oldpassword != ''){
      const errorMessage = 'Not Same Password';
      const errorElement = document.getElementById('error-message-Login');
      errorElement.innerText = errorMessage;
      errorElement.style.display = 'block';
      return;
    }
    else if(pseudo != '' && oldpassword == ''){
      const errorMessage = 'Please enter your atcually password for change your pseudo';
      const errorElement = document.getElementById('error-message-Login');
      errorElement.innerText = errorMessage;
      errorElement.style.display = 'block';
      return;
    }

    const formData = {
        oldpassword: oldpassword,
    };

    if (pseudo != '')
    {
      formData.pseudo = pseudo;
    }

    if (password != '')
    {
      formData.password = password;
    }

    console.log(formData);

    
    const jsonString = JSON.stringify(formData);
    
    const url = '/api/users/user/';

    const options = {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: jsonString
      };

      fetch(url, options)
      .then(response => {
       
        return response.json();
      })
      .then(updatedData => {
        console.log('Data updated:', updatedData);
      })

}


