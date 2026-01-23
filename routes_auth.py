from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models import db, Utilisateur
from flask_bcrypt import Bcrypt

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']
        mot_de_passe = bcrypt.generate_password_hash(request.form['mot_de_passe']).decode('utf-8')
        role = request.form['role']

        user = Utilisateur(nom=nom, email=email, mot_de_passe=mot_de_passe, role=role)
        db.session.add(user)
        db.session.commit()
        flash("Inscription réussie !", "success")
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']
        user = Utilisateur.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.mot_de_passe, mot_de_passe):
            login_user(user)
            flash("Connexion réussie !", "success")
            if user.role == "admin":
                return redirect(url_for('dashboard_admin'))
            elif user.role == "enseignant":
                return redirect(url_for('dashboard_enseignant'))
            else:
                return redirect(url_for('dashboard_candidat'))
        else:
            flash("Email ou mot de passe incorrect", "danger")
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Déconnexion réussie", "info")
    return redirect(url_for('auth.login'))