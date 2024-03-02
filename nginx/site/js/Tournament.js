import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Tournament");

    }

    async executeViewScript()
    {

      console.log("TESTTTT Event listen OK")
    
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