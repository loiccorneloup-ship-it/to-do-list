document.addEventListener('DOMContentLoaded', () => {
    // Initialisation du Drag & Drop pour chaque colonne
    document.querySelectorAll('.task-list').forEach(el => {
        new Sortable(el, {
            group: 'shared',
            animation: 150,
            handle: '.drag-handle',
            onEnd: (evt) => {
                const id = evt.item.getAttribute('data-id');
                const newColId = evt.to.id.replace('col-', '');
                // Optionnel : tu peux ajouter un fetch ici pour sauver la position
            }
        });
    });
});

function openEditModal(id, titre, desc) {
    document.getElementById('editModal').style.display = 'block';
    document.getElementById('editTitre').value = titre;
    document.getElementById('editDesc').value = desc;
    document.getElementById('editTaskForm').action = '/modifier_tache/' + id;
}

function closeModal() {
    document.getElementById('editModal').style.display = 'none';
}

function editColumnTitle(id, currentTitle) {
    let nouveau = prompt("Nouveau nom pour cette liste :", currentTitle);
    if (nouveau && nouveau.trim() !== "") {
        let f = document.createElement('form');
        f.method = 'POST'; f.action = '/modifier_colonne/' + id;
        let i = document.createElement('input');
        i.name = 'nouveau_titre'; i.value = nouveau;
        f.appendChild(i); document.body.appendChild(f);
        f.submit();
    }
}