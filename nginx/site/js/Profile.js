import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Profile");

    }

    async executeViewScript()
    {

      EventProfile();
      document.getElementById("btnLogout").addEventListener('click', EventLogout);
      //EventProfile()

      document.getElementById("TournamentButton").addEventListener('click',event  => {
        window.history.pushState(null, "Tournament", "/tournament/");
        window.dispatchEvent(new Event('popstate'));
      }); 
      document.getElementById("OnlineGameButton").addEventListener('click',event  => {
        window.history.pushState(null, "Online", "/online/");
        window.dispatchEvent(new Event('popstate'));
      });  
      document.getElementById("LocalGameButton").addEventListener('click',event  => {
        window.history.pushState(null, "local", "/local/");
        window.dispatchEvent(new Event('popstate'));
      });   
      document.getElementById("ButtonChange").addEventListener('click', EventChange);
      document.getElementById("flexSwitchTwoFA").addEventListener('click', EventActiveTwoFA);
      document.getElementById("btnScoreboard").addEventListener('click', getUserStats);
    
    }

    async getHtml() {
      try{
        const response = await fetch('/profile.html');
        if (!response.ok){
            throw new Error('Failed to fetch profile.html');
        }
        const html = await response.text();
        return html;
      } catch(error){
        console.error('Error fetchin', error);
        return '<p>Error loading </p>'
      }
    }
}