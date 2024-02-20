import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Register");

    }

    async executeViewScript()
    {
      //console.log("Register Charge");

    }
    
    async getHtml() {
      try{
        const response = await fetch('https://localhost/register.html');
        if (!response.ok){
            throw new Error('Failed to fetch Register.html');
        }
        const html = await response.text();
        return html;
        } catch(error){
          console.error('Error fetchin', error);
          return '<p>Error loading </p>'
        }
    }
}