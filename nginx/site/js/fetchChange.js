async function EventChange () {
    const CurrentPseudo = document.querySelector('#ActuallyPseudo').value;
    const Newpseudo = document.querySelector('#ChangePseudo').value;
    const  oldpassword  = document.querySelector('#OldPassword').value;
    const  password  = document.querySelector('#ChangePassword').value;
    const  confirmpassword  = document.querySelector('#ConfirmChangePassword').value;

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
    else if(Newpseudo != '' && oldpassword == ''){
      const errorMessage = 'Please enter your actually password for change your pseudo';
      const errorElement = document.getElementById('error-message-Login');
      errorElement.innerText = errorMessage;
      errorElement.style.display = 'block';
      return;
    }else if (CurrentPseudo === '' && Newpseudo != ''){
      const errorMessage = 'Please enter your actually pseudo for change your pseudo';
      const errorElement = document.getElementById('error-message-Login');
      errorElement.innerText = errorMessage;
      errorElement.style.display = 'block';
      return;
    }

      const userresponse = await fetch('/api/users/user/', {
          method: 'GET',
          headers: {
              'Content-Type': 'application/json',
          }
      });

      const userData = await userresponse.json();
      if (userData.data.pseudo != CurrentPseudo){
        const errorMessage = 'Please enter your actually pseudo for change your pseudo';
        const errorElement = document.getElementById('error-message-Login');
        errorElement.innerText = errorMessage;
        errorElement.style.display = 'block';
      }


    const formData = {
        oldpassword: oldpassword,
    };

    if (Newpseudo != '')
    {
      formData.pseudo = Newpseudo;
    }

    if (password != '')
    {
      formData.password = password;
    }

    

    const jsonString = JSON.stringify(formData);

    console.log(jsonString);
    
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
       
        console.log(response.json());
      })
      .then(updatedData => {
        console.log('Data updated:', updatedData);
      })

}


