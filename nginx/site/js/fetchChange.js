async function EventChange () {
    const CurrentPseudo = document.querySelector('#ActuallyPseudo').value;
    const  oldpassword  = document.querySelector('#OldPassword').value;
    const  password  = document.querySelector('#ChangePassword').value;
    const  confirmpassword  = document.querySelector('#ConfirmChangePassword').value;


    let myModalEl = document.getElementById('modalProfile');
    let modal = bootstrap.Modal.getInstance(myModalEl);


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


