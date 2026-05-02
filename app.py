# Importation des outils nécessaires
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# CONFIGURATION : On dit à Flask d'utiliser une base SQLite nommée 'taches.db'
# [cite: 25] Le sujet impose de stocker les données (Base de données SQLite ici)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taches.db'
db = SQLAlchemy(app)

# MODÈLE DE DONNÉES : Structure de la table 'Tache' dans la base
# [cite: 8] Chaque tâche doit contenir les champs imposés par le PDF
class Tache(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Identifiant unique automatique
    titre = db.Column(db.String(100), nullable=False) # [cite: 9] Champ obligatoire
    description = db.Column(db.String(255)) # [cite: 10] Détails de la tâche
    fait = db.Column(db.Boolean, default=False) # [cite: 11] Statut binaire (Vrai/Faux)
    date_fin = db.Column(db.String(50)) # [cite: 12] Date limite
    colonne_id = db.Column(db.Integer, default=1) # Permet de classer dans AC1, AC2 ou AC3

# MODÈLE DE DONNÉES : Pour pouvoir renommer les titres des colonnes
class Colonne(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(50), nullable=False)

# INITIALISATION : Crée les tables si elles n'existent pas au lancement
with app.app_context():
    db.create_all()
    # Si la base est vide, on crée par défaut les 3 colonnes du Kanban
    if not Colonne.query.first():
        db.session.add_all([Colonne(titre="AC1"), Colonne(titre="AC2"), Colonne(titre="AC3")])
        db.session.commit()

# ROUTE PRINCIPALE : Affiche la page d'accueil [cite: 20]
@app.route('/')
def index():
    # On récupère toutes les tâches et toutes les colonnes pour les envoyer au HTML
    taches = Tache.query.all() 
    colonnes = Colonne.query.all()
    return render_template('index.html', taches=taches, colonnes=colonnes)

# ROUTE AJOUTER : Récupère les infos du formulaire et crée une entrée [cite: 19]
@app.route('/ajouter', methods=['POST'])
def ajouter():
    # 'request.form.get' récupère les données envoyées par les balises <input> du HTML
    nouvelle = Tache(
        titre=request.form.get('titre'),
        description=request.form.get('description'),
        date_fin=request.form.get('date_fin'),
        colonne_id=int(request.form.get('colonne_id'))
    )
    db.session.add(nouvelle) # Prépare l'insertion
    db.session.commit() # [cite: 24] Sauvegarde définitivement dans le fichier .db
    return redirect(url_for('index')) # Rafraîchit la page pour voir la nouvelle tâche

# ROUTE MODIFIER : Met à jour le titre et la description [cite: 21]
@app.route('/modifier_tache/<int:id>', methods=['POST'])
def modifier_tache(id):
    tache = Tache.query.get_or_404(id) # Trouve la tâche ou renvoie une erreur 404
    tache.titre = request.form.get('titre')
    tache.description = request.form.get('description')
    db.session.commit() # Enregistre les modifications
    return redirect(url_for('index'))

# ROUTE STATUT : Alterne entre 'Fait' et 'À faire' [cite: 23]
@app.route('/toggle_tache/<int:id>')
def toggle_tache(id):
    tache = Tache.query.get_or_404(id)
    tache.fait = not tache.fait # Si c'était True, ça devient False (et inversement)
    db.session.commit()
    return redirect(url_for('index'))

# ROUTE SUPPRIMER : Retire une tâche de la base [cite: 22]
@app.route('/supprimer/<int:id>', methods=['POST'])
def supprimer(id):
    tache = Tache.query.get_or_404(id)
    db.session.delete(tache)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) # Lance le serveur en mode 'développement'