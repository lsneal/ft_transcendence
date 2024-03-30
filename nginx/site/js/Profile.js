import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Profile");
    }

    async executeViewScript() {

        document.getElementById("btnLogout").addEventListener('click', EventLogout);

        let isAuthenticated = false;

        try {
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
                isAuthenticated = false; 
            } else {
                isAuthenticated = true; 
            }
        } catch (error) {
        }

        if (isAuthenticated === false) {
            return; 
        }

        EventProfile();
      
        //EventProfile()

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
        document.getElementById("ButtonChange").addEventListener('click', EventChange);
        document.getElementById("flexSwitchTwoFA").addEventListener('click', EventGetQRCode);

        document.getElementById("Valid2FA").addEventListener('click', EventActiveTwoFA);
        document.getElementById("btnScoreboard").addEventListener('click', getUserStats);
        document.getElementById("confirmDisable2FA").addEventListener('click', EventDisableTwoFA);
        document.getElementById("btnDropdown2").addEventListener('click', getHistoricOnline);
        
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
