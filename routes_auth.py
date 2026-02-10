from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models import db, Utilisateur
from flask_bcrypt import Bcrypt

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

# =========================
# REGISTER
# =========================
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nom = request.form['nom']
        cin = request.form['cin']   # nouveau champ CIN
        role = "candidat"           # rôle imposé par défaut

        user = Utilisateur(nom=nom, cin=cin, role=role)
        db.session.add(user)
        db.session.commit()
        flash("Inscription réussie !", "success")
        return redirect(url_for('auth.login'))
    return render_template('register.html')


# =========================
# LOGIN
# =========================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nom = request.form['nom']
        cin = request.form['cin']

        user = Utilisateur.query.filter_by(nom=nom, cin=cin).first()
        if user:
            login_user(user)
            flash("Connexion réussie !", "success")
            if user.role == "admin":
                return redirect(url_for('dashboard_admin'))
            elif user.role == "enseignant":
                return redirect(url_for('dashboard_enseignant'))
            else:
                return redirect(url_for('dashboard_candidat'))
        else:
            flash("Nom ou CIN incorrect", "danger")
    return render_template('login.html')


# =========================
# LOGOUT
# =========================
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Déconnexion réussie", "info")
    return redirect(url_for('auth.login'))