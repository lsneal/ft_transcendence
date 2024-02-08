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

        return ` 
        <div class="container text-center">
  <div class="row align-items-start">
        <div class="btn-group btn-group-lg" role="group" aria-label="Large button group">
            <button type="button" data-bs-toggle="modal" data-bs-target="#modalA class="btn btn-outline-dark">Left</button>
            <button type="button" class="btn btn-outline-dark">Middle</button>
            <button type="button" class="btn btn-outline-dark">Right</button>
        </div>
        </div>
        </div>

        <div class="modal fade modal-xl" id="modalA" tabindex="-1" aria-labelledby="modalScoreboard" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-body"></div>
            
          </div>
        </div>
      </div>
        `;
    }
}