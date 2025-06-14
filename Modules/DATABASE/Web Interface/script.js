document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.menu-toggle');
    const dashboardContainer = document.querySelector('.dashboard-container');
    const refreshButton = document.querySelector('.header-right .material-icons-outlined[title="Actualiser les données"]');


    // Toggle la classe 'sidebar-open' sur le conteneur du tableau de bord
    if (menuToggle && dashboardContainer) {
        menuToggle.addEventListener('click', function() {
            dashboardContainer.classList.toggle('sidebar-open');
        });
    }

    // Gérer l'état actif des éléments de navigation de la sidebar
    const navItems = document.querySelectorAll('.sidebar-nav .nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', function(event) {
            // event.preventDefault(); // Décommenter si tu gères le routage via JS (SPA)

            navItems.forEach(nav => nav.classList.remove('active'));
            this.classList.add('active');

            if (window.innerWidth <= 768) {
                dashboardContainer.classList.remove('sidebar-open');
            }
        });
    });


    // --- NOUVEAU : Fonction pour simuler la mise à jour des données Docker ---
    // En réalité, cette fonction ferait une requête AJAX/Fetch à ton backend
    // pour récupérer les vraies données Docker.
    function updateDockerStats() {
        console.log("Actualisation des données Docker...");
        // Simuler une requête API avec un délai
        setTimeout(() => {
            // Mettre à jour les valeurs dans le DOM
            document.getElementById('running-containers').textContent = Math.floor(Math.random() * 10) + 1; // Ex: entre 1 et 10
            document.getElementById('stopped-containers').textContent = Math.floor(Math.random() * 5); // Ex: entre 0 et 5
            document.getElementById('avg-cpu').textContent = (Math.random() * 20 + 5).toFixed(1) + '%'; // Ex: entre 5 et 25%
            document.getElementById('total-images').textContent = Math.floor(Math.random() * 50) + 10; // Ex: entre 10 et 60

            // Mise à jour de la barre de progression (disque)
            const diskUsage = Math.floor(Math.random() * 80) + 10; // entre 10 et 90%
            document.querySelector('.progress-bar-fill').style.width = diskUsage + '%';
            document.querySelector('.progress-text').textContent = `${diskUsage}% (Données Sim.)`;

            // Ici, tu mettrais à jour dynamiquement le tableau des conteneurs
            // Exemple : tu viderais #container-list-body et le remplirais avec des <tr> générés par JS
            // en fonction des données reçues de ton backend.
            // Par simplicité, nous ne le faisons pas pour cette maquette HTML statique.
            console.log("Données Docker mises à jour !");

        }, 1500); // Simule un délai de 1.5 secondes pour la requête
    }

    // --- NOUVEAU : Gérer le bouton d'actualisation ---
    if (refreshButton) {
        refreshButton.addEventListener('click', updateDockerStats);
    }

    // --- NOUVEAU : Appeler l'actualisation au chargement de la page pour les données initiales ---
    updateDockerStats();
});