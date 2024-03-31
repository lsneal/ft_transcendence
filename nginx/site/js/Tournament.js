import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Tournament");

    }

    async executeViewScript()
    {
      const container = document.querySelector('#body');
      function clearSpheres() {
        const spheres = document.querySelectorAll('.sphere');
        spheres.forEach(sphere => {
          sphere.remove();
        });
      }

      clearSpheres();

      try {
          const userresponse = await fetch('/api/users/user/', {
              method: 'GET',
              headers: {
                  'Content-Type': 'application/json',
              }
          });

          const userData = await userresponse.json();

          if (userData.detail === "Unauthenticated!") {
              window.history.pushState(null, "Logout", "/");
              window.dispatchEvent(new Event('popstate'));
          }
      } catch (error) {
      }

      document.getElementById("btnLogout").addEventListener('click', EventLogout);
    

      if (window.innerWidth < 1288 && window.innerWidth > 606)
      {
        document.getElementById("game").style.display = 'block';
        document.getElementById("game").style.width = "500px";
        document.getElementById("leftBox").style.left = "0%";
        document.getElementById("rightBox").style.left = "95.1%";
      }
      else if (window.innerWidth < 606)
      {
        document.getElementById("game").style.display = 'none';
      }



      document.getElementById("logoenhaut").addEventListener('click', event => {
        window.history.pushState(null, "Profile", "/profile/");
        window.dispatchEvent(new Event('popstate'));
      });
     
     
      document.getElementById("btnScoreboard").addEventListener('click', getUserStats);

    }


    async getHtml() {
      try{
        const response = await fetch('/Tournament.html');
        if (!response.ok){
            throw new Error('Failed to fetch Home.html');
        }
        const html = await response.text();
        return html;
      } catch(error){
        console.error('Error fetchin', error);
        return '<p>Error loading </p>'
      }
    }
}