import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Local");

    }

    async executeViewScript()
    {


      document.getElementById("btnLogout").addEventListener('click', EventLogout);


      
      if (window.innerWidth < 1288 && window.innerWidth > 606)
      {
        document.getElementById("game-container").style.display = 'block';
        document.getElementById("game").style.width = "500px";
        document.getElementById("leftBox").style.left = "0%";
        document.getElementById("rightBox").style.left = "95.1%";
        document.getElementById("time").style.fontSize = '1.0rem';
      }
      else if (window.innerWidth < 606)
      {
        document.getElementById("game-container").style.display = 'none';
      }
    }


    async getHtml() {
      try{
        const response = await fetch('/LocalGame.html');
        if (!response.ok){
            throw new Error('Failed to fetch LocalGame.html');
        }
        const html = await response.text();
        return html;
      } catch(error){
        console.error('Error fetchin', error);
        return '<p>Error loading </p>'
      }
    }
}