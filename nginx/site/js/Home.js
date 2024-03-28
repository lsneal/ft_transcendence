import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Home");

    }

    async executeViewScript()
    {

      try {
        const userresponse = await fetch('/api/users/user/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        const userData = await userresponse.json();
        if (userData.detail != "Unauthenticated!") {
          window.history.pushState(null, "Profile", "/profile/");
          window.dispatchEvent(new Event('popstate'));
        }
      }catch(error){
        console.error('Erreur: ', error.message)
      }



      document.getElementById("Validlogin2fa").addEventListener('click', send2facode);

      document.getElementById("btnRegister").addEventListener('click', EventRegister);
      
      document.getElementById('modalRegistrer').addEventListener('keydown', function(event) {
        if (event.key === "Enter") {
          document.getElementById('btnRegister').click();
        }
      });

      document.getElementById("btnLogin").addEventListener('click', EventLogin);
     
      document.getElementById('modalEmail').addEventListener('keydown', function(event) {
        if (event.key === "Enter") {
          document.getElementById('btnLogin').click();
        }
      });

      document.getElementById("BtnRank").addEventListener('click', getRankingPlayers);

     
    }

    async getHtml() {
      try{
        const response = await fetch('/home.html');
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