// --- CONFIGURATION ---
let tempsRestant = 1800; // 30 minutes en secondes (à ajuster selon tes besoins)

// --- CHRONOMÈTRE ---
function lancerChrono() {
    const affichage = document.getElementById('timer');
    if (!affichage) return; // Sécurité si l'élément n'existe pas sur la page

    const intervalle = setInterval(() => {
        let minutes = Math.floor(tempsRestant / 60);
        let secondes = tempsRestant % 60;

        // Formatage 00:00
        affichage.textContent = `${minutes}:${secondes < 10 ? '0' : ''}${secondes}`;

        if (tempsRestant <= 0) {
            clearInterval(intervalle);
            alert("Temps écoulé ! Votre examen va être soumis automatiquement.");
            document.getElementById('examen-form').submit(); // Soumission automatique
        }
        tempsRestant--;
    }, 1000);
}

// --- SAUVEGARDE AUTOMATIQUE (AJAX) ---
// Cette fonction s'exécute à chaque clic sur une réponse
function sauvegarderReponse(questionId, choixId) {
    console.log(`Enregistrement : Question ${questionId}, Réponse ${choixId}`);
    
    // Envoi des données au serveur Flask sans recharger la page
    fetch('/sauvegarder_reponse', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id_question: questionId,
            id_choix: choixId
        })
    })
    .then(response => {
        if (response.ok) {
            console.log("Données sécurisées sur le serveur.");
        }
    })
    .catch(error => console.error("Erreur de connexion :", error));
}

// Lancement au chargement de la page
window.onload = lancerChrono;