# routes_exam.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

exam_bp = Blueprint('exam', __name__)

@exam_bp.route('/exam')
@login_required
def exam():
    if current_user.role != "candidat":
        flash("Accès réservé aux candidats uniquement.", "warning")
        if current_user.role == "admin":
            return redirect(url_for("dashboard_admin"))
        elif current_user.role == "enseignant":
            return redirect(url_for("dashboard_enseignant"))
        else:
            return redirect(url_for("auth.login"))
    return render_template("exam.html", title="Session d'Examen")