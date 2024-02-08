import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Home");
    }

    async getHtml() {
        return ` 
        <section id="content_box"></section>
        <!-- MAIN CONTENT -->
        
        <div class="container">
    
            <div class="row justify-content-center main-buttons">    
              <div class="col-6">
                <div><button id="Buttonlogin" data-bs-toggle="modal" data-bs-target="#modalLogin" type="button" class="btn btn-lg btn-warning mb-3 w-100">Login</button></div>
                <div><button id="ButtonRegistrer" data-bs-toggle="modal" data-bs-target="#modalRegistrer" type="button" class="btn btn-lg btn-warning mb-3 w-100">Registrer</button></div>
                <div><button id="ButtonScoreboard" data-bs-toggle="modal" data-bs-target="#modalScoreboard" type="button" class="btn btn-lg btn-warning w-100">Scoreboard</button></div>
              </div>
            </div>
          </div>


    <!-- MODAL LOGIN -->
    <div class="modal fade" id="modalLogin" tabindex="-1" aria-labelledby="modalLogin" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
         
          <div class="modal-body">
          <div><button type="button"  data-bs-toggle="modal" data-bs-target="#modal42" class="btn btn-lg btn-outline-warning mb-3 w-100"><i class="fa-solid fa-at"></i>   with email</button></div>
          </div>
         
        </div>
      </div>
    </div>

    <!-- MODAL REGITRER -->
    <div class="modal fade" id="modalRegistrer" tabindex="-1" aria-labelledby="modalRegistrer" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-body">

            <form class="row g-3">
              <div class="col-md-6">
                <label for="validationDefault03" class="form-label">email</label>
                <input type="text" class="form-control" id="validationDefault03" required>
              </div>
              <div class="col-md-4">
                <label for="validationDefaultUsername" class="form-label">Username</label>
                <div class="input-group">
                  <span class="input-group-text" id="inputGroupPrepend2">@</span>
                  <input type="text" class="form-control" id="validationDefaultUsername" aria-describedby="inputGroupPrepend2" required>
                </div>
              </div>
              <div class="col-md-4">
                <label for="validationDefault05" class="form-label">Password</label>
                <input type="password" class="form-control" id="validationDefault05" required>
              </div>
              <div class="col-md-4">
                <label for="validationDefault05" class="form-label">Confirm Password</label>
                <input type="password" class="form-control" id="validationDefault05" required>
              </div>
              <div class="col-12">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" value="" id="invalidCheck2" required>
                  <label class="form-check-label" for="invalidCheck2">
                    Agree to terms and conditions
                  </label>
                </div>
              </div>
              <div class="col-12">
                <a href="/api/register/" class="btn btn-primary" type="submit" role="button" data-link >Submit form</a>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

  <!-- MODAL LOGIN EMAIL-->
  <div class="modal fade" id="modal42" tabindex="-1" aria-labelledby="modal42" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
       
        <div class="modal-body">
          <form>
            <div class="mb-3">
              <label for="exampleInputEmail1" class="form-label">Email address</label>
              <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp">
              <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
            </div>
            <div class="mb-3">
              <label for="exampleInputPassword1" class="form-label">Password</label>
              <input type="password" class="form-control" id="exampleInputPassword1">
            </div>
            <div class="mb-3 form-check">
              <input type="checkbox" class="form-check-input" id="exampleCheck1">
              <label class="form-check-label" for="exampleCheck1">Check me out</label>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
          </form>
        </div>
       
      </div>
    </div>
  </div>

    <!-- MODAL SCORE -->
    <div class="modal fade modal-xl" id="modalScoreboard" tabindex="-1" aria-labelledby="modalScoreboard" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-body"></div>
        </div>
      </div>
    </div>
        `;
    }
}