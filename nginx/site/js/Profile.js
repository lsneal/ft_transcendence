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
  
      if (userData.detail === "Unauthenticated!" || window.location.href.indexOf('profile') < -1) {
          window.history.pushState(null, "Home", "/home");
          window.dispatchEvent(new Event('popstate'));
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
  
  
      document.getElementById('modalProfile').addEventListener('keydown', function(event) {
          if (event.key === "Enter") {
            buttonChange.click();
          }
        });
  
      document.getElementById('modaltwoFA').addEventListener('keydown', function(event) {
          if (event.key === "Enter") {
            valid2FA.click();
          }
        });
  
      // Création des bulles
      /*const container = document.querySelector('#body');
  
      function clearSpheres() {
        const spheres = document.querySelectorAll('.sphere');
        spheres.forEach(sphere => {
          sphere.remove();
        });
      }

      clearSpheres();
      
      function clearBubbles() {
        const bubbles = document.querySelectorAll('.bubble');
        bubbles.forEach(bubble => {
          bubble.remove();
        });
      }
  
      clearBubbles();
  
      function createBubble() {
        const bubble = document.createElement('div');
        bubble.classList.add('bubble');
        bubble.style.left = `${Math.random() * container.offsetWidth}px`;
        bubble.style.bottom = '0';
        container.appendChild(bubble);
  
        const speed = 2 + Math.random() * 2;
  
        function moveBubble() {
          const bottom = parseFloat(bubble.style.bottom);
          if (bottom >= container.offsetHeight) {
            bubble.remove();
            return;
          }
          bubble.style.bottom = `${bottom + speed}px`;
          requestAnimationFrame(moveBubble);
        }
  
        moveBubble();
      }
  
      // Création de 10 bulles
      for (let i = 0; i < 30; i++) {
        createBubble();
      }*/
  
      // Création des sphères
      /*function createSphere(x, y, speedX, speedY, className) {
        const sphere = document.createElement('div');
        sphere.className = `sphere ${className}`;
        container.appendChild(sphere);
  
        function moveSphere() {
          x += speedX;
          y += speedY;
  
          const radius = parseInt(getComputedStyle(sphere).width) / 2;
  
          if (x + radius >= container.offsetWidth || x - radius <= 0) {
            speedX *= -1;
          }
          if (y + radius >= container.offsetHeight || y - radius <= 0) {
            speedY *= -1;
          }
  
          sphere.style.left = `${x - radius}px`;
          sphere.style.top = `${y - radius}px`;
  
          requestAnimationFrame(moveSphere);
        }
  
        moveSphere();
      }*/
  
      //createSphere(container.offsetWidth / 4, container.offsetHeight / 2, 3, 3, 'sphere1');
  
      //createSphere(container.offsetWidth / 2, container.offsetHeight / 4, -3, -2, 'sphere2');
  
      //createSphere(container.offsetWidth / 2, container.offsetHeight / 5, 1, 3, 'sphere3');
  
      //createSphere(container.offsetWidth / 4, container.offsetHeight / 4, -2, 6, 'sphere4');
  
      //createSphere(container.offsetWidth / 3, container.offsetHeight / 3, -1, 4, 'sphere5');
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
