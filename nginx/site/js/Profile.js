import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Profile");

    }

    async executeViewScript()
    {
      console.log("Logout Button Charge")
      document.getElementById("btnLogout").addEventListener('click', EventLogout);
      EventProfile();
    }

    async getHtml() {
      try{
        const response = await fetch('https://localhost/profile.html');
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