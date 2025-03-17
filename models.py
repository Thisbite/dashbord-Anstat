from flask_sqlalchemy import SQLAlchemy

# Initialisation de SQLAlchemy (sera liée à l'application Flask dans votre code principal)
db = SQLAlchemy()

# Modèle pour la table 'Region'
class Region(db.Model):
    __tablename__ = 'Region'

    region_id = db.Column(db.Integer, primary_key=True)
    f_direction_stat_id = db.Column(db.Integer, db.ForeignKey('DirectionStatistique.id'), nullable=True)
    nom_region = db.Column(db.Text, nullable=False)

    # Relation avec DirectionStatistique
    direction_stat = db.relationship('DirectionStatistique', backref='regions')

    def __repr__(self):
        return f"<Region(region_id={self.region_id}, nom_region={self.nom_region})>"

# Modèle pour la table 'indicateur_v2'
class IndicateurV2(db.Model):
    __tablename__ = 'indicateur_v2'

    indicateur_id = db.Column(db.Integer, primary_key=True)
    indicateur = db.Column(db.Text, nullable=False)
    definitions = db.Column(db.Text, nullable=True)  # Longtext mappé à Text dans SQLAlchemy
    mode_calcul = db.Column(db.Text, nullable=True)  # Longtext mappé à Text dans SQLAlchemy

    def __repr__(self):
        return f"<IndicateurV2(indicateur_id={self.indicateur_id}, indicateur={self.indicateur})>"

# Modèle pour la table 'V1_indicateur'
class V1Indicateur(db.Model):
    __tablename__ = 'V1_indicateur'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Dimension = db.Column(db.String(255), nullable=True)
    Modalites = db.Column(db.String(255), nullable=True)
    Indicateurs = db.Column(db.String(255), nullable=True)
    Annee = db.Column(db.String(25), nullable=True)
    Valeur = db.Column(db.DECIMAL(15, 2), nullable=True)
    Region = db.Column(db.String(45), nullable=True)  # Pas de clé étrangère explicite ici

    def __repr__(self):
        return f"<V1Indicateur(id={self.id}, Indicateurs={self.Indicateurs}, Annee={self.Annee})>"

# Modèle pour la table 'Indicateur'
class Indicateur(db.Model):
    __tablename__ = 'Indicateur'

    indicateur_id = db.Column(db.Integer, primary_key=True)
    f_domaine_id = db.Column(db.Integer, nullable=True)  # Pas de table Domaine fournie, donc pas de ForeignKey
    nom_indicateur = db.Column(db.Text, nullable=False)
    definition = db.Column(db.Text, nullable=True)  # Longtext mappé à Text
    mode_calcul = db.Column(db.Text, nullable=True)  # Longtext mappé à Text

    def __repr__(self):
        return f"<Indicateur(indicateur_id={self.indicateur_id}, nom_indicateur={self.nom_indicateur})>"

# Modèle pour la table 'DirectionStatistique'
class DirectionStatistique(db.Model):
    __tablename__ = 'DirectionStatistique'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<DirectionStatistique(id={self.id}, nom={self.nom})>"