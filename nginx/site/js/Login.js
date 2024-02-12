import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Login");

    }


    async getHtml() {
      try{
        const response = await fetch('https://localhost/Login.html');
        if (!response.ok){
            throw new Error('Failed to fetch Login.html');
        }
        const html = await response.text();
        return html;
      } catch(error){
        console.error('Error fetchin', error);
        return '<p>Error loading </p>'
      }
    }
}