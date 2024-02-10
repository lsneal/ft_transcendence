import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Register");

        var myModalEl = document.getElementById('modalRegistrer');
        var modal = bootstrap.Modal.getInstance(myModalEl)
        modal.hide();
    }
    
    async getHtml() {
      try{
        const response = await fetch('./Register.html');
        if (!response.ok){
            throw new Error('Failed to fetch Register.html');
        }
        const html = await response.text();
        return html;
        } catch(error){
          console.error('Error fetchin', error);
          return '<p>Error loading </p>'
        }
       
        ;
    }
}