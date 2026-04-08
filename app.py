from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taches.db'
db = SQLAlchemy(app)

# Table pour les tâches [cite: 25]
class Tache(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False) # [cite: 9]
    description = db.Column(db.String(255)) # [cite: 10]
    fait = db.Column(db.Boolean, default=False) # [cite: 11]
    date_fin = db.Column(db.String(50)) # [cite: 12]
    colonne_id = db.Column(db.Integer, default=1) # AC1, AC2 ou AC3

# Table pour les titres des listes (AC1, AC2, AC3)
class Colonne(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()
    # Initialisation des colonnes si vides
    if not Colonne.query.first():
        db.session.add_all([Colonne(titre="AC1"), Colonne(titre="AC2"), Colonne(titre="AC3")])
        db.session.commit()

@app.route('/')
def index():
    taches = Tache.query.all() # [cite: 20]
    colonnes = Colonne.query.all()
    return render_template('index.html', taches=taches, colonnes=colonnes)

@app.route('/ajouter', methods=['POST']) # [cite: 19]
def ajouter():
    nouvelle = Tache(
        titre=request.form.get('titre'),
        description=request.form.get('description'),
        date_fin=request.form.get('date_fin'),
        colonne_id=int(request.form.get('colonne_id'))
    )
    db.session.add(nouvelle)
    db.session.commit() # [cite: 24]
    return redirect(url_for('index'))

@app.route('/modifier_tache/<int:id>', methods=['POST']) # 
def modifier_tache(id):
    tache = Tache.query.get_or_404(id)
    tache.titre = request.form.get('titre')
    tache.description = request.form.get('description')
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/toggle_tache/<int:id>') # 
def toggle_tache(id):
    tache = Tache.query.get_or_404(id)
    tache.fait = not tache.fait
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/modifier_colonne/<int:id>', methods=['POST'])
def modifier_colonne(id):
    col = Colonne.query.get_or_404(id)
    col.titre = request.form.get('nouveau_titre')
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/supprimer/<int:id>', methods=['POST']) # [cite: 22]
def supprimer(id):
    tache = Tache.query.get_or_404(id)
    db.session.delete(tache)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)