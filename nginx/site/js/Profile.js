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

        if (isAuthenticated === false || window.location.href.indexOf('profile') < -1) {
            return; 
        }
        
        let tournamentButton = document.getElementById("TournamentButton");
        let onlineButton = document.getElementById("OnlineGameButton");
        let localButton = document.getElementById("LocalGameButton");
        if (tournamentButton)
        {
            tournamentButton.addEventListener('click', event => {
                window.history.pushState(null, "Tournament", "/tournament/");
                window.dispatchEvent(new Event('popstate'));
            });
        }
        if (onlineButton)
        {
            onlineButton.addEventListener('click', event => {
                window.history.pushState(null, "Online", "/online/");
                window.dispatchEvent(new Event('popstate'));
            });
        }
        if (localButton)
        {
            localButton.addEventListener('click', event => {
                window.history.pushState(null, "local", "/local/");
                window.dispatchEvent(new Event('popstate'));
            });
        }

        let buttonChange = document.getElementById("ButtonChange");
        let flexSwitchTwoFA = document.getElementById("flexSwitchTwoFA");
        let valid2FA = document.getElementById("Valid2FA");
        let btnScoreboard = document.getElementById("btnScoreboard");
        let confirmDisable2FA = document.getElementById("confirmDisable2FA");
        let btnDropdown2 = document.getElementById("btnDropdown2");
        if (buttonChange) {buttonChange.addEventListener('click', EventChange);}
        if (flexSwitchTwoFA) {flexSwitchTwoFA.addEventListener('click', EventGetQRCode);}
        if (valid2FA) {valid2FA.addEventListener('click', EventActiveTwoFA);}
        if (btnScoreboard) {btnScoreboard.addEventListener('click', getUserStats);}
        if (confirmDisable2FA) {confirmDisable2FA.addEventListener('click', EventDisableTwoFA);}
        if (btnDropdown2) {btnDropdown2.addEventListener('click', getHistoricOnline);}
        

        
        
        
        
        
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
