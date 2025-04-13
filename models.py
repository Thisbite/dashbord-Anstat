from app import db

class Domaine(db.Model):
    __tablename__ = 'Domaines'
    idDomaines = db.Column(db.String(10), primary_key=True)
    nomDomaines = db.Column(db.String(255), nullable=False)

    sous_domaines = db.relationship('SousDomaine', backref='domaine', lazy=True)

class SousDomaine(db.Model):
    __tablename__ = 'Sous_Domaines'
    idSousDomaines = db.Column(db.String(10), primary_key=True)
    f_idDomaines = db.Column(db.String(10), db.ForeignKey('Domaines.idDomaines'), nullable=False)
    nomSousDomaines = db.Column(db.String(255), nullable=False)

    indicateurs = db.relationship('Indicateur', backref='sous_domaine', lazy=True)

class Indicateur(db.Model):
    __tablename__ = 'Indicateurs'
    idIndicateurs = db.Column(db.String(10), primary_key=True)
    f_idSousDomaines = db.Column(db.String(10), db.ForeignKey('Sous_Domaines.idSousDomaines'))
    nomIndicateur = db.Column(db.String(255), nullable=False)
    definition = db.Column(db.Text)

    donnees = db.relationship('Donnee', backref='indicateur', lazy=True)

class Annee(db.Model):
    __tablename__ = 'Annees'
    idAnnees = db.Column(db.String(10), primary_key=True)
    valAnnees = db.Column(db.Integer, nullable=False)

    donnees = db.relationship('Donnee', backref='annee', lazy=True)

class Dimension(db.Model):
    __tablename__ = 'Dimensions'
    idDimensions = db.Column(db.String(10), primary_key=True)
    nomDimension = db.Column(db.String(255), nullable=False)

    modalites = db.relationship('Modalite', backref='dimension', lazy=True)

class Modalite(db.Model):
    __tablename__ = 'Modalites'
    idModalites = db.Column(db.String(10), primary_key=True)
    f_idDimensions = db.Column(db.String(10), db.ForeignKey('Dimensions.idDimensions'))
    nomModalites = db.Column(db.String(255), nullable=False)

    donnees_modalites = db.relationship('DonneeModalite', backref='modalite', lazy=True)

class Donnee(db.Model):
    __tablename__ = 'Donnees'
    idDonnees = db.Column(db.Integer, primary_key=True, autoincrement=True)
    f_idIndicateurs = db.Column(db.String(10), db.ForeignKey('Indicateurs.idIndicateurs'), nullable=False)
    f_idAnnees = db.Column(db.String(10), db.ForeignKey('Annees.idAnnees'), nullable=False)
    valDonnees = db.Column(db.Numeric(10, 2))

    donnees_modalites = db.relationship('DonneeModalite', backref='donnee', lazy=True)

class DonneeModalite(db.Model):
    __tablename__ = 'Donnees_modalites'
    idDonnees_modalites = db.Column(db.Integer, primary_key=True, autoincrement=True)
    f_idDonnees = db.Column(db.Integer, db.ForeignKey('Donnees.idDonnees'))
    f_idModalites = db.Column(db.String(10), db.ForeignKey('Modalites.idModalites'))

    __table_args__ = (
        db.UniqueConstraint('f_idDonnees', 'f_idModalites', name='unique_donnee_modalite'),
    )
