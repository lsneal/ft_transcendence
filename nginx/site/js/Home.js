import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Home");

    }


    checkLog(){
      const userresponse =  fetch('/api/users/user/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then((userresponse) => userresponse.json())
    .then((data) =>{
      if (data.detail != "Unauthenticated!") {
        window.history.pushState(null, "Profile", "/profile/");
        window.dispatchEvent(new Event('popstate'));
      }
    });
    }

    async executeViewScript()
    {
      this.checkLog()
      
      document.getElementById("Validlogin2fa").addEventListener('click', send2facode);

      document.getElementById("btnRegister").addEventListener('click', EventRegister);
      
      document.getElementById('modalRegistrer').addEventListener('keydown', function(event) {
        if (event.key === "Enter") {
          document.getElementById('btnRegister').click();
        }
      });

      document.getElementById("btnLogin").addEventListener('click', EventLogin);
     
      document.getElementById('modalEmail').addEventListener('keydown', function(event) {
        if (event.key === "Enter") {
          document.getElementById('btnLogin').click();
        }
      });

      document.getElementById("BtnRank").addEventListener('click', getRankingPlayers);

    
      const container = document.querySelector('#body');
  
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
      }
  
      // Création des sphères
      function createSphere(x, y, speedX, speedY, className) {
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
      }
  
      createSphere(container.offsetWidth / 4, container.offsetHeight / 2, 3, 3, 'sphere1');
  
      createSphere(container.offsetWidth / 2, container.offsetHeight / 4, -3, -2, 'sphere2');
  
      createSphere(container.offsetWidth / 2, container.offsetHeight / 5, 1, 3, 'sphere3');
  
      createSphere(container.offsetWidth / 4, container.offsetHeight / 4, -2, 6, 'sphere4');
  
      createSphere(container.offsetWidth / 3, container.offsetHeight / 3, -1, 4, 'sphere5');
    }

    async getHtml() {
      try{
        const response = await fetch('/home.html');
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