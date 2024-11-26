// Gestion de la navigation dans la barre latérale
document.querySelectorAll('.menu-item').forEach(item => {
    item.addEventListener('click', function(e) {
        e.preventDefault();

        // Supprime l'état "active" de tous les éléments
        document.querySelectorAll('.menu-item').forEach(el => el.classList.remove('active'));

        // Ajoute l'état "active" à l'élément cliqué
        this.classList.add('active');

        // Masque toutes les sections
        document.querySelectorAll('.section').forEach(section => section.classList.add('hidden'));

        // Affiche la section correspondante
        const target = this.getAttribute('data-target');
        document.getElementById(target).classList.remove('hidden');
    });
});