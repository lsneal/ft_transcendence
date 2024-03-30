async function EventChange () {
    const CurrentPseudo = document.querySelector('#ActuallyPseudo').value;
    const  oldpassword  = document.querySelector('#OldPassword').value;
    const  password  = document.querySelector('#ChangePassword').value;
    const  confirmpassword  = document.querySelector('#ConfirmChangePassword').value;


    let myModalEl = document.getElementById('modalProfile');
    let modal = bootstrap.Modal.getInstance(myModalEl);

    if (!CurrentPseudo || !password) {
      const errorMessage = 'Password or pseudo is empty';
      const errorElement = document.getElementById('error-message-Login');
      errorElement.innerText = errorMessage;
      errorElement.style.display = 'block';
      return;
    }
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
    if (password && password === confirmpassword) {
      if (password.length < 6) {
        const errorMessage = 'Password length must be greater than 6 character';
        const errorElement = document.getElementById('error-message-Login');
        errorElement.innerText = errorMessage;
        errorElement.style.display = 'block';
        return;
      }

    }
      const userresponse = await fetch('/api/users/user/', {
          method: 'GET',
          headers: {
              'Content-Type': 'application/json',
          }
      });

      const userData = await userresponse.json();
      if (userData.data.pseudo != CurrentPseudo){
        const errorMessage = 'Please enter your pseudo for change your password';
        const errorElement = document.getElementById('error-message-Login');
        errorElement.innerText = errorMessage;
        errorElement.style.display = 'block';
        modal.show();
        return;
      }


    const formData = {
        oldpassword: oldpassword,
        pseudo: CurrentPseudo,
        password: password,
    };
    
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
    .then(data => {
        if (data === 'Wrong Password'){
          const errorMessage = 'Wrong Actual Password';
          const errorElement = document.getElementById('error-message-Login');
          errorElement.innerText = errorMessage;
          errorElement.style.display = 'block';
        }
        else{
          document.querySelector('#ActuallyPseudo').value = '';
          document.querySelector('#OldPassword').value = '';
          document.querySelector('#ChangePassword').value = '';
          document.querySelector('#ConfirmChangePassword').value = '';
          modal.hide()
        }
    })
    .catch(error => {
    });

}


