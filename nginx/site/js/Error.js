import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Error");

    }

    async executeViewScript()
    {

    async function EventError() {
      window.history.pushState(null, "Error", "/");
                window.dispatchEvent(new Event('popstate'));

      };
    document.getElementById("image404").addEventListener('click', EventError);
    }


    async getHtml() {
      try{
        const response = await fetch('/error.html');
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