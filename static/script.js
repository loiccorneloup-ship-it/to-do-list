document.addEventListener('DOMContentLoaded', () => {
    // DRAG & DROP : On initialise la bibliothèque Sortable sur chaque liste de tâches
    document.querySelectorAll('.task-list').forEach(el => {
        new Sortable(el, {
            group: 'shared', // Permet de déplacer une tâche d'une colonne à une autre
            animation: 150,  // Effet fluide lors du déplacement
            handle: '.drag-handle', // On ne peut attraper la tâche que par le symbole '⠿'
            onEnd: (evt) => {
                // Ici, on pourrait ajouter un appel 'fetch' pour sauver la nouvelle colonne en base
                const id = evt.item.getAttribute('data-id');
                console.log("Tâche déplacée : " + id);
            }
        });
    });
});

// MODALE : Affiche la fenêtre de modification et remplit les champs avec les données actuelles
function openEditModal(id, titre, desc) {
    document.getElementById('editModal').style.display = 'block'; // Affiche la div cachée
    document.getElementById('editTitre').value = titre;
    document.getElementById('editDesc').value = desc;
    // On modifie dynamiquement l'URL du formulaire pour viser la bonne tâche
    document.getElementById('editTaskForm').action = '/modifier_tache/' + id;
}

// MODALE : Cache la fenêtre
function closeModal() {
    document.getElementById('editModal').style.display = 'none';
}

// TITRE LISTE : Permet de renommer AC1, AC2, etc. via une boîte de dialogue
function editColumnTitle(id, currentTitle) {
    let nouveau = prompt("Nouveau nom pour cette liste :", currentTitle);
    if (nouveau && nouveau.trim() !== "") {
        // On crée un formulaire invisible pour envoyer la donnée au serveur Python
        let f = document.createElement('form');
        f.method = 'POST'; 
        f.action = '/modifier_colonne/' + id;
        let i = document.createElement('input');
        i.name = 'nouveau_titre'; i.value = nouveau;
        f.appendChild(i); 
        document.body.appendChild(f);
        f.submit(); // Envoi des données vers app.py
    }
}