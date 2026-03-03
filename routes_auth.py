from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, Utilisateur

auth_bp = Blueprint('auth', __name__)

# =========================
# REGISTER
# =========================
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        # ⚡ Rediriger vers la page index si déjà connecté
        return redirect(url_for('pages.index'))

    if request.method == 'POST':
        nom = request.form.get('nom')
        cin = request.form.get('cin')
        role = request.form.get('role', 'candidat')  # rôle choisi ou par défaut candidat

        # Vérifier si l'utilisateur existe déjà
        user_exist = Utilisateur.query.filter_by(cin=cin).first()
        if user_exist:
            flash("Ce CIN existe déjà.", "danger")
            return redirect(url_for('auth.register'))

        user = Utilisateur(nom=nom, cin=cin, role=role)
        db.session.add(user)
        db.session.commit()

        flash("Inscription réussie !", "success")
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


# =========================
# LOGIN
# =========================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Redirection intelligente si déjà connecté
        if current_user.role == "admin":
            return redirect(url_for("dashboard.admin"))
        elif current_user.role == "enseignant":
            return redirect(url_for("dashboard.enseignant"))
        elif current_user.role == "candidat":
            return redirect(url_for("dashboard.candidat"))

    if request.method == 'POST':
        nom = request.form.get('nom')
        cin = request.form.get('cin')

        user = Utilisateur.query.filter_by(nom=nom, cin=cin).first()

        if user:
            login_user(user)
            flash("Connexion réussie !", "success")

            # 🔐 Redirection selon le rôle
            if user.role == "admin":
                return redirect(url_for("dashboard.admin"))

            elif user.role == "enseignant":
                return redirect(url_for("dashboard.enseignant"))

            elif user.role == "candidat":
                return redirect(url_for("dashboard.candidat"))

            else:
                return redirect(url_for("pages.index"))

        else:
            flash("Nom ou CIN incorrect", "danger")

    return render_template('auth/login.html')

# =========================
# LOGOUT
# =========================
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Déconnexion réussie", "info")
    return redirect(url_for('auth.login'))
