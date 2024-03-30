import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Profile");
    }

    async executeViewScript() {

        document.getElementById("btnLogout").addEventListener('click', EventLogout);


            const userresponse = await fetch('/api/users/user/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const userData = await userresponse.json();

            if (userData.detail === "Unauthenticated!") {
                window.history.pushState(null, "Home", "/home");
                window.dispatchEvent(new Event('popstate'));
            }

        EventProfile();
      

        document.getElementById("TournamentButton").addEventListener('click', event => {
            window.history.pushState(null, "Tournament", "/tournament/");
            window.dispatchEvent(new Event('popstate'));
        });
        document.getElementById("OnlineGameButton").addEventListener('click', event => {
            window.history.pushState(null, "Online", "/online/");
            window.dispatchEvent(new Event('popstate'));
        });
        document.getElementById("LocalGameButton").addEventListener('click', event => {
            window.history.pushState(null, "local", "/local/");
            window.dispatchEvent(new Event('popstate'));
        });

        document.getElementById("flexSwitchTwoFA").addEventListener('click', EventGetQRCode);
        document.getElementById("btnScoreboard").addEventListener('click', getUserStats);
        document.getElementById("btnDropdown2").addEventListener('click', getHistoricOnline);

        
        document.getElementById("ButtonChange").addEventListener('click', EventChange);
        document.getElementById('modalProfile').addEventListener('keydown', function(event) {
            if (event.key === "Enter") {
              document.getElementById('ButtonChange').click();
            }
          });


        document.getElementById("Valid2FA").addEventListener('click', EventActiveTwoFA);
        document.getElementById('modaltwoFA').addEventListener('keydown', function(event) {
            if (event.key === "Enter") {
              document.getElementById('Valid2FA').click();
            }
          });

        document.getElementById("confirmDisable2FA").addEventListener('click', EventDisableTwoFA);
        
    }

    async getHtml() {
        try {
            const response = await fetch('/profile.html');
            if (!response.ok) {
                throw new Error('Failed to fetch profile.html');
            }
            const html = await response.text();
            return html;
        } catch (error) {
            console.error('Error fetching', error);
            return '<p>Error loading </p>'
        }
    }
}
