from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# -------------------
# Utilisateur commun
# -------------------
class Utilisateur(UserMixin, db.Model):
    __tablename__ = 'utilisateur'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin / enseignant / candidat

    # Relations
    candidat = db.relationship('Candidat', backref='utilisateur', uselist=False)
    enseignant = db.relationship('Enseignant', backref='utilisateur', uselist=False)

# -------------------
# Candidat
# -------------------
class Candidat(db.Model):
    __tablename__ = 'candidat'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), unique=True)

    resultats = db.relationship('Resultat', backref='candidat', lazy=True)

# -------------------
# Enseignant
# -------------------
class Enseignant(db.Model):
    __tablename__ = 'enseignant'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), unique=True)

# -------------------
# Concours
# -------------------
class Concours(db.Model):
    __tablename__ = 'concours'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)

    examens = db.relationship('Examen', backref='concours', lazy=True)

# -------------------
# Module
# -------------------
class Module(db.Model):
    __tablename__ = 'module'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)

    examens = db.relationship('Examen', backref='module', lazy=True)

# -------------------
# Examen
# -------------------
class Examen(db.Model):
    __tablename__ = 'examen'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    duree = db.Column(db.Integer, nullable=False)  # en minutes
    concours_id = db.Column(db.Integer, db.ForeignKey('concours.id'))
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))

    questions = db.relationship('Question', backref='examen', lazy=True)
    resultats = db.relationship('Resultat', backref='examen', lazy=True)

# -------------------
# Question
# -------------------
class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    enonce = db.Column(db.Text, nullable=False)
    examen_id = db.Column(db.Integer, db.ForeignKey('examen.id'))

    reponses = db.relationship('Reponse', backref='question', lazy=True)

# -------------------
# Reponse
# -------------------
class Reponse(db.Model):
    __tablename__ = 'reponse'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    texte = db.Column(db.Text, nullable=False)
    correcte = db.Column(db.Boolean, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

# -------------------
# Resultat
# -------------------
class Resultat(db.Model):
    __tablename__ = 'resultat'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    score = db.Column(db.Float, nullable=False)
    date_passage = db.Column(db.DateTime, default=db.func.current_timestamp())
    candidat_id = db.Column(db.Integer, db.ForeignKey('candidat.id'))
    examen_id = db.Column(db.Integer, db.ForeignKey('examen.id'))