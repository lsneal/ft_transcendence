/* On récupère les éléments form et message */
const form = document.getElementById("formRegister");
const message = document.getElementById("message");

/* Lors de la soumission du formulaire on previent
le comportement par défaut */
form.addEventListener("submit", async function (e) {
  e.preventDefault();

  /* L'astuce pour IE, si vous n'utilisez pas de polyfill, consiste
  à inviter l'utilisateur à utiliser un autre navigateur */
  if (!window.fetch || !window.FormData) {
    alert(
      "Tu crois que c'est du respect mon garçon ? Est ce que tu crois que c'est du respect d'utiliser un navigateur archaïque ?"
    );
    return;
  }

  /* Lorsque l'on instancie FormData on peut lui passer un élément
  form en paramètre. De cette façon, FormData peut detecter chaque
  input du formulaire et leur valeur.
  Ici, this fait référence à form */
  const formData = new FormData(this);

  try {
    /* fetch() prend en 1er paramètre l'url et en second paramètre
    les options. Ici, nous indiquons que notre requête sera en POST
    et que le corps de la requête sera constitué de nos formData. */
    await fetch("http://localhost:3000/register", {
      method: "POST",
      body: formData,
    });

    // On affiche un message suivant le résultat de la requête
    message.innerText = "Fichier uploadé avec succès \\o/";
  } catch (error) {
    message.innerText =
      "C'est la cata, c'est la cata, c'est la catastrophe /o\\";
  }

  // On réinitialise le formulaire
  this.reset();

  // On efface le message après deux secondes
  setTimeout(() => {
    message.innerText = "";
  }, 2000);
});