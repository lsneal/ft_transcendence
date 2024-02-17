import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Home");

        console.log("Home");
    }

    async executeViewScript()
    {
      //console.log("Modal Charge")

      document.getElementById("btnRegister").addEventListener('click', EventRegister);
      document.getElementById("btnLogin").addEventListener('click', EventLogin);
     
    }

    async getHtml() {
      try{
        const response = await fetch('https://localhost/home.html');
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