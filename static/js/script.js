// Gestion des données factices pour les descriptions des domaines
const descriptionsDomaines = {
    "Population": "Le domaine de la population couvre les statistiques relatives à l'état et structure de la population; la dynamique de la population (mariages, divorces, taille des ménages); les perspectives démographiques.",
    "Agriculture": "Le domaine de l'agriculture couvre les statistiques relatives à la production végétale; la production forestière et chasse; la production animale et halieutique; l'aménagement rural.",
    "Condition de vie des ménages": "Le domaine de la condition de vie des ménages couvre les statisitques permettant d'évaluer le bien-être économique et social des populations : éducation; santé; emploi par grands domaines; logement; revenu, consommation, budget; protection sociale; culture et loisirs.",
    "Entreprises non Agricoles": "Le domaine des entreprises non agricoles couvre les statistiques relatives aux bâtiments et travaux Publics; mines et industries; commerce et services; eau et électricité; transports; poste et télécoms; tourisme et artisanat.",
    "Environnement": "Le domaine de l'environnement couvres les statistiques relatives aux ressources naturelles et biodiversité; établissements humains; catastrophes naturelles et risque.",
    "Gouvernance": "Le domaine de la gouvernance couvres les statistiques relatives au statistique politique; Economique; Sociale; Judiciaire; Institutionnelle; Participative.",
    "Grands Equilibres Economiques": "Le domaine des grands équilibres économiques couvre les statistiques relatives au secteur réel (PIB,Exportations et importations de biens et services physiques); Monnaie et crédit; aux échanges extérieurs; Finances publiques."
  };
  
  // Variable globale pour stocker les domaines
  let domaines = {};
  
  // Initialisation de la page
  document.addEventListener('DOMContentLoaded', () => {
    console.log("JavaScript chargé !");
  
    // Gestion du menu hamburger
    const menuToggle = document.getElementById('menu-toggle');
    const menuIcon = document.getElementById('menu-icon');
    const navLinks = document.getElementById('nav-links');
    const menuOverlay = document.getElementById('menu-overlay');
    let isMenuOpen = false;
  
    console.log("Menu toggle:", menuToggle);
    console.log("Nav links:", navLinks);
  
    // Vérifier si on est sur desktop (≥768px)
    const isDesktop = window.matchMedia("(min-width: 768px)").matches;
    if (isDesktop) {
      navLinks.classList.add('open'); // S'assurer que le menu est visible sur desktop
    }
  
    menuToggle.addEventListener('click', () => {
      console.log("Bouton hamburger cliqué !");
      isMenuOpen = !isMenuOpen;
      if (isMenuOpen) {
        navLinks.classList.add('open');
      } else {
        navLinks.classList.remove('open');
      }
      menuIcon.classList.toggle('fa-bars');
      menuIcon.classList.toggle('fa-times');
      menuOverlay.classList.toggle('active');
      menuToggle.setAttribute('aria-label', isMenuOpen ? 'Fermer le menu' : 'Ouvrir le menu');
      console.log("Menu ouvert:", isMenuOpen);
    });
  
    // Fermer le menu si on clique à l'extérieur
    document.addEventListener('click', (e) => {
      if (!menuToggle.contains(e.target) && !navLinks.contains(e.target) && isMenuOpen) {
        isMenuOpen = false;
        navLinks.classList.remove('open');
        menuIcon.classList.add('fa-bars');
        menuIcon.classList.remove('fa-times');
        menuOverlay.classList.remove('active');
        menuToggle.setAttribute('aria-label', 'Ouvrir le menu');
      }
    });
  
    // Fermer le menu avec la touche "Escape"
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && isMenuOpen) {
        isMenuOpen = false;
        navLinks.classList.remove('open');
        menuIcon.classList.add('fa-bars');
        menuIcon.classList.remove('fa-times');
        menuOverlay.classList.remove('active');
        menuToggle.setAttribute('aria-label', 'Ouvrir le menu');
      }
    });
  
    // Gérer le redimensionnement de la fenêtre
    window.addEventListener('resize', () => {
      const isDesktopNow = window.matchMedia("(min-width: 768px)").matches;
      if (isDesktopNow) {
        navLinks.classList.add('open'); // S'assurer que le menu est visible sur desktop
        menuOverlay.classList.remove('active'); // Désactiver l'overlay
        menuIcon.classList.add('fa-bars');
        menuIcon.classList.remove('fa-times');
        isMenuOpen = false;
      }
    });
  
    // Gestion de la modale et du backdrop
    const descriptionModal = document.getElementById('descriptionModal');
    const modalBackdrop = document.getElementById('modalBackdrop');
  
    // Afficher la modale et le backdrop au chargement
    descriptionModal.classList.remove('hidden');
    descriptionModal.classList.add('show');
    modalBackdrop.classList.remove('hidden');
    modalBackdrop.classList.add('show');
  
    // Fermer la modale et le backdrop
    document.querySelectorAll('[data-bs-dismiss="modal"]').forEach(btn => {
      btn.addEventListener('click', () => {
        descriptionModal.classList.remove('show');
        descriptionModal.classList.add('hidden');
        modalBackdrop.classList.remove('show');
        modalBackdrop.classList.add('hidden');
      });
    });
  
    // Fermer la modale et le backdrop avec la touche "Escape"
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !descriptionModal.classList.contains('hidden')) {
        descriptionModal.classList.remove('show');
        descriptionModal.classList.add('hidden');
        modalBackdrop.classList.remove('show');
        modalBackdrop.classList.add('hidden');
      }
    });
  
    // Autocomplétion pour la barre de recherche
    const searchInput = document.getElementById("search-input");
    const suggestionsContainer = document.getElementById("suggestions");
  
    searchInput.addEventListener("input", async () => {
      const query = searchInput.value.trim();
      if (query.length < 2) {
        suggestionsContainer.innerHTML = "";
        suggestionsContainer.classList.add('hidden');
        return;
      }
  
      try {
        const response = await fetch(`/autocomplete?query=${encodeURIComponent(query)}`);
        const data = await response.json();
        suggestionsContainer.innerHTML = "";
        if (data.length > 0) {
          suggestionsContainer.classList.remove('hidden');
          data.forEach(item => {
            const div = document.createElement("div");
            div.textContent = item;
            div.classList.add('p-2');
            div.onclick = () => {
              searchInput.value = item;
              suggestionsContainer.innerHTML = "";
              suggestionsContainer.classList.add('hidden');
              window.location.href = `/search_indicators2/${encodeURIComponent(item)}`;
            };
            suggestionsContainer.appendChild(div);
          });
        } else {
          suggestionsContainer.classList.add('hidden');
        }
      } catch (error) {
        console.error('Erreur lors de l\'autocomplétion:', error);
        suggestionsContainer.classList.add('hidden');
      }
    });
  
    document.addEventListener("click", (event) => {
      if (!searchInput.contains(event.target) && !suggestionsContainer.contains(event.target)) {
        suggestionsContainer.innerHTML = "";
        suggestionsContainer.classList.add('hidden');
      }
    });
  
    // Filtrage des indicateurs
    const indicatorSearch = document.getElementById('indicatorSearch');
    const clearSearchBtn = document.getElementById('clearSearch');
    const indicateursList = document.getElementById('indicateurs');
  
    indicatorSearch.addEventListener('input', () => {
      const query = indicatorSearch.value.toLowerCase().trim();
      filterIndicators(query);
    });
  
    clearSearchBtn.addEventListener('click', () => {
      indicatorSearch.value = '';
      filterIndicators('');
    });
  
    function filterIndicators(query) {
      const indicatorItems = indicateursList.getElementsByClassName('list-group-item');
      for (let item of indicatorItems) {
        const indicatorText = item.textContent.toLowerCase();
        if (indicatorText.includes(query)) {
          item.classList.remove('hidden');
        } else {
          item.classList.add('hidden');
        }
      }
    }
  
    // Chargement des données
    fetchData();
  });
  
  // Fonction pour soumettre la recherche
  function submitSearch() {
    const searchInput = document.getElementById("search-input");
    const query = searchInput.value.trim();
    if (query.length < 2) {
      alert("Veuillez entrer au moins 2 caractères pour la recherche.");
      return false;
    }
    return true;
  }
  
  // Récupération des données
  async function fetchData() {
    try {
      const response = await fetch('/get_data2');
      const data = await response.json();
      Object.keys(data).forEach(key => {
        const [domaine, thematique] = key.split(', ');
        if (!domaines[domaine]) {
          domaines[domaine] = { thematiques: {} };
        }
        domaines[domaine].thematiques[thematique] = data[key];
      });
      displayDomaines();
      const firstDomaine = Object.keys(domaines)[0];
      if (firstDomaine) selectDomaine(firstDomaine);
    } catch (error) {
      console.error('Erreur lors de la récupération des données:', error);
    }
  }
  
  // Affichage des domaines
  function displayDomaines() {
    const domainesList = document.getElementById('domaines');
    domainesList.innerHTML = '';
    Object.keys(domaines).forEach(domaine => {
      const li = document.createElement('li');
      li.classList.add('list-group-item', 'flex', 'items-center', 'space-x-2', 'p-3', 'rounded-lg');
      li.innerHTML = `<i class="fas fa-folder text-primary"></i> <span>${domaine.charAt(0).toUpperCase() + domaine.slice(1).replace(/_/g, ' ')}</span>`;
      li.onclick = () => selectDomaine(domaine);
      domainesList.appendChild(li);
    });
  }
  
  // Sélection d'un domaine
  function selectDomaine(domaine) {
    const domainesList = document.getElementById('domaines');
    const allDomaines = domainesList.querySelectorAll('li');
    allDomaines.forEach(li => li.classList.remove('active'));
    const selectedDomaine = Array.from(allDomaines).find(li => li.textContent.trim().toLowerCase() === domaine.toLowerCase());
    if (selectedDomaine) selectedDomaine.classList.add('active');
  
    const btnEnSavoirPlus = document.getElementById('btn-en-savoir-plus');
    // Mettre à jour le texte du bouton avec le nom du domaine
    btnEnSavoirPlus.textContent = `Informations sur ${domaine.charAt(0).toUpperCase() + domaine.slice(1).replace(/_/g, ' ')}`;
    btnEnSavoirPlus.classList.remove('hidden');
    btnEnSavoirPlus.onclick = () => afficherInfosDomaine(domaine);
    afficherInfosDomaine(domaine);
  
    const thematiquesList = document.getElementById('thematiques');
    const indicateursList = document.getElementById('indicateurs'); // Correction de la faute de frappe
    thematiquesList.innerHTML = '';
    indicateursList.innerHTML = '';
  
    if (!domaines[domaine]) {
      console.error(`Le domaine ${domaine} n'existe pas.`);
      return;
    }
  
    Object.keys(domaines[domaine].thematiques).forEach(thematique => {
      const li = document.createElement('li');
      li.classList.add('list-group-item', 'flex', 'items-center', 'space-x-2', 'p-3', 'rounded-lg');
      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.classList.add('form-check-input', 'h-5', 'w-5', 'text-primary');
      checkbox.id = thematique;
      checkbox.onchange = () => toggleIndicateurs(domaine, thematique, checkbox.checked);
      const label = document.createElement('label');
      label.classList.add('checkbox-label', 'cursor-pointer');
      label.setAttribute('for', thematique);
      label.textContent = thematique.charAt(0).toUpperCase() + thematique.slice(1);
      li.appendChild(checkbox);
      li.appendChild(label);
      thematiquesList.appendChild(li);
    });
  }
  
  // Afficher/masquer les indicateurs
  function toggleIndicateurs(domaine, thematique, isChecked) {
    const indicateursList = document.getElementById('indicateurs');
    if (isChecked) {
      domaines[domaine].thematiques[thematique].forEach(indicateur => {
        const li = document.createElement('li');
        li.classList.add('list-group-item', 'p-3', 'rounded-lg');
        li.id = `indicateur-${indicateur.replace(/\s+/g, '-')}`;
        const a = document.createElement('a');
        a.href = `#`;
        a.textContent = indicateur;
        a.classList.add('indicateur-link');
        li.appendChild(a);
        indicateursList.appendChild(li);
        a.onclick = (e) => {
          e.preventDefault();
          searchIndicatorInElastic(indicateur);
        };
  
        const currentQuery = document.getElementById('indicatorSearch').value.toLowerCase().trim();
        if (currentQuery && !indicateur.toLowerCase().includes(currentQuery)) {
          li.classList.add('hidden');
        }
      });
    } else {
      domaines[domaine].thematiques[thematique].forEach(indicateur => {
        const li = document.getElementById(`indicateur-${indicateur.replace(/\s+/g, '-')}`);
        if (li) indicateursList.removeChild(li);
      });
    }
  }
  
  // Recherche d'un indicateur
  function searchIndicatorInElastic(indicateur) {
    const encodedIndicateur = encodeURIComponent(indicateur);
    window.location.href = `/search_indicators2/${encodedIndicateur}`;
  }
  
  // Afficher les informations sur le domaine
  function afficherInfosDomaine(domaine) {
    const domaineInfo = document.getElementById('domaine-info');
    const domaineDescription = document.getElementById('domaine-description');
    domaineDescription.textContent = descriptionsDomaines[domaine] || "Aucune description disponible pour ce domaine.";
    domaineInfo.classList.remove('hidden');
  }