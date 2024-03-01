import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Tournament");

    }

    async executeViewScript()
    {
      if (window.innerWidth < 1288)
      {
        document.getElementById("game").style.width = "500px";
      }
    }


    async getHtml() {
      try{
        const response = await fetch('https://localhost/Tournament.html');
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