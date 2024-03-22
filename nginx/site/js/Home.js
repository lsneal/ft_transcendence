import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Home");

        console.log("Home");
    }

    async executeViewScript()
    {
      document.getElementById("btnLogin42").addEventListener('click', EventLogin42);

      document.getElementById("btnRegister").addEventListener('click', EventRegister);
      // Handle enter in modal
      document.getElementById('modalRegistrer').addEventListener('keydown', function(event) {
        if (event.key === "Enter") {
          document.getElementById('btnRegister').click();
        }
      });

      document.getElementById("btnLogin").addEventListener('click', EventLogin);
      // Handle enter in modal
      document.getElementById('modalEmail').addEventListener('keydown', function(event) {
        if (event.key === "Enter") {
          document.getElementById('btnLogin').click();
        }
      });

      document.getElementById("BtnRank").addEventListener('click', getRankingPlayers);
      document.getElementById("modallogin2fa").addEventListener('click', send2facode);


      // Handle redirection error when wrong url
      /*if (window.location != 'https://localhost/')
      {
        window.history.pushState(null, "Error Page 404", "/error/");
        window.dispatchEvent(new Event('popstate'));
      }*/
     
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