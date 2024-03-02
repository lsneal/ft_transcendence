import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Tournament");

    }

    async executeViewScript()
    {

      console.log("TESTTTT Event listen OK")
      console.log(window.innerWidth)
      if (window.innerWidth < 1288)
      {
        document.getElementById("game").style.width = "500px";
      }
    }


    async getHtml() {
      try{
        const response = await fetch('/LocalGame.html');
        if (!response.ok){
            throw new Error('Failed to fetch LocalGame.html');
        }
//        if (window.innerWidth < 612)
//          throw new Error('Small Window LocalGame.html');

        const html = await response.text();
        return html;
      } catch(error){
        console.error('Error fetchin', error);
        return '<p>Error loading </p>'
      }
    }
}